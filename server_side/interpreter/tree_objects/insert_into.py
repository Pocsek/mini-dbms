from server_side.interpreter.tree_objects.executable_tree import ExecutableTree


class InsertInto(ExecutableTree):
    """
    Represents an INSERT INTO command.
    Examples:
        INSERT INTO table_name (column1, column2, column3) VALUES (value1, value2, value3), (value4, value5, value6)
        INSERT INTO table_name VALUES (value1, value2, value3), (value4, value5, value6)
    """

    def __init__(self):
        super().__init__()
        self.__table_name: str = ""
        self.__column_names: list[str] = []
        self.__values: list[list[str]] = []  # a list where a value is a record to be inserted, a record is a list

    def _execute(self, dbm):
        db_idx = dbm.get_working_db_index()
        table_idx = dbm.find_table(db_idx, self.__table_name)
        db = dbm.get_working_db()
        table = db.get_tables()[table_idx]
        records = self.__make_records()
        dbm.insert(db, table, records)

    def validate(self, dbm, **kwargs):
        """
        In the future it should be dependent on constraints, and type validation.

        For example:
        - identity
        - primary key
        - default
        -etc.
        """
        # check if all values are valid

        db = dbm.get_working_db()
        table = db.get_table(self.__table_name)
        if table is None:
            raise ValueError(f"Table [{self.__table_name}] does not exist in the database.")
        existing_column_names = table.get_column_names()
        if len(self.__column_names) != 0:
            # if column names are specified, validate them
            self.__validate_column_names(existing_column_names)
        else:
            # if column names are not specified, use the existing column names
            self.__column_names = existing_column_names

        # TODO:
        #  - if identity is declared, remove column with identity from column names
        #  - create a system database that stores system level data e.g.: last identity value of a table
        # identity_col = table.get_identity_column()
        # if identity_col:
        #     self.__column_names.remove(identity_col.get_name())

        self.__validate_values(dbm, db, table)  # validate the values

    def connect_nodes_to_root(self):
        pass

    def connect_subtrees_to_root(self):
        pass

    def set_table_name(self, table_name: str):
        self.__table_name = table_name

    def get_table_name(self) -> str:
        return self.__table_name

    def add_column_name(self, column_name: str):
        self.__column_names.append(column_name)

    def get_column_names(self) -> list[str]:
        return self.__column_names

    def add_value(self, value: list[str]):
        self.__values.append(value)

    def get_values(self) -> list[list[str]]:
        return self.__values

    def __validate_column_names(self, existing_column_names: list[str]):
        """
        Check if all column names are valid and not repeated.
        """
        for col_name in self.__column_names:
            if col_name not in existing_column_names:
                raise ValueError(f"Column [{col_name}] does not exist in the table.")
            if self.__column_names.count(col_name) > 1:
                raise ValueError(f"Column [{col_name}] is repeated.")

    def __validate_values(self, dbm, db, table):
        """
        Check if all values are valid and the number of values is equal to the number of column names.
        """
        columns = [table.get_column(col_name) for col_name in self.__column_names]
        required_nr_values = len(self.__column_names)
        for record in self.__values:
            if len(record) != required_nr_values:
                raise ValueError(f"Expected {required_nr_values} values, found {len(record)}.")
            # TODO: handle case where table has identity column

            # check if the types are correct
            for i, to_insert in enumerate(record):
                if not self.__matches_type(to_insert, columns[i]):
                    raise ValueError(f"Value [{to_insert}] does not match the type of column [{columns[i].get_name()}].")

            # check integrity of the record to be inserted
            self.__validate_primary_key(dbm, db, table, record)
            self.__validate_unique_keys(dbm, db, table, record)
            self.__validate_foreign_keys(dbm, db, table, record)

    def __validate_primary_key(self, dbm, db, table, record):
        """
        Validate primary key integrity, i.e. the record to be inserted is unique to the primary key.
        """
        # if the primary key is not compound and has identity, then it is valid for sure and we can simply return
        identity_col = table.get_identity_column()
        pk_col_names = table.get_primary_key().get_column_names()
        if identity_col and len(pk_col_names) == 1:
            if identity_col.get_name() == pk_col_names[0]:
                return
        # if an entry with the same primary key exists in the table, raise an error
        pk_col_values = self.__get_column_values(pk_col_names, record)
        if dbm.find_by_primary_key(db.get_name(), table.get_name(), pk_col_values):
            raise ValueError(f"Primary key [{pk_col_values}] already exists in the table.")

    def __validate_unique_keys(self, dbm, db, table, record):
        """
        For each unique key, validate unique key integrity, i.e. the value to be inserted is unique to the unique key.
        """
        # if an entry with the same unique key exists in the table, raise an error
        for uq in table.get_unique_keys():
            col_names = uq.get_column_names()
            col_values = self.__get_column_values(col_names, record)
            if dbm.find_by_value(db.get_name(), table.get_name(), col_names, col_values):
                raise ValueError(f"Unique key [{col_names}] with value [{col_values}] already exists in the table.")

    def __validate_foreign_keys(self, dbm, db, table, record):
        """
        For each foreign key, validate foreign key integrity, i.e. the value to be inserted appears in the parent table.
        """
        # upon inserting into a child table, if the inserted key does not exist in the parent table, raise an error
        for fk in table.get_foreign_keys():
            to_insert_col_names = fk.get_source_column_names()
            to_insert_col_values = self.__get_column_values(to_insert_col_names, record)
            ref_table_name = fk.get_referenced_table_name()
            ref_col_names = fk.get_referenced_column_names()

            ok = True
            ref_table = dbm.get_table(dbm.get_working_db_index(), ref_table_name)
            if ref_table.is_primary_key(ref_col_names):
                # the referenced key is a primary key: find by primary key
                if not dbm.find_by_primary_key(db.get_name(), ref_table_name, to_insert_col_values):
                    ok = False
            else:
                # the referenced key is a unique key: find by unique key
                if not dbm.find_by_value(db.get_name(), ref_table_name, to_insert_col_names, to_insert_col_values):
                    ok = False
            if not ok:
                raise ValueError(
                    (f"Foreign key [{to_insert_col_names}] with value [{to_insert_col_values}] does not exist in the "
                     f"referenced table [{ref_table_name}].")
                )

    def __get_column_values(self, column_names, record) -> list:
        col_values = []
        for i in range(len(self.__column_names)):
            if self.__column_names[i] in column_names:
                col_values.append(record[i])
        return col_values

    def __matches_type(self, val, column) -> bool:
        # TODO: extract this function into a class dedicated to datatypes
        """
        Check if the value matches the type of the column.
        """
        col_type = column.get_type()
        match col_type:
            case "int":
                return val.isdigit()
            case "float":
                return isinstance(val, float)
            case "varchar":
                return isinstance(val, str)
            case _:
                raise ValueError(f"Unknown datatype '{col_type}'.")

    def __make_records(self) -> list[dict]:
        """
        Pair the column names with the values to create records.

        No validation is done here.
        """
        records = []
        for value in self.__values:
            record = {}
            for col_name, val in zip(self.__column_names, value):
                record[col_name] = val
            records.append(record)
        return records
