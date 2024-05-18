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

    def _execute(self, dbm=None):
        db_idx = dbm.get_working_db_index()
        table_idx = dbm.find_table(db_idx, self.__table_name)
        db = dbm.get_working_db()
        table = db.get_tables()[table_idx]
        records = self.__make_records()
        dbm.insert(db, table, records)

    def validate(self, dbm=None):
        """
        In the future it should be dependent on constraints, and type validation.

        For example:
        - identity
        - primary key
        - default
        -etc.
        """
        # check if all values are valid
        # if identity is set the column can't be inserted -> won't be implemented in the first version
        db_idx = dbm.get_working_db_index()
        table_idx = dbm.find_table(db_idx, self.__table_name)
        if table_idx == -1:
            raise ValueError(f"Table [{self.__table_name}] does not exist in the database.")
        existing_column_names = dbm.get_column_names(db_idx, table_idx)
        if len(self.__column_names) != 0:
            # if column names are specified, validate them
            self.__validate_column_names(existing_column_names)
        else:
            # if column names are not specified, use the existing column names
            self.__column_names = existing_column_names
        self.__validate_values()  # validate the values

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

    def __validate_values(self):
        """
        Check if all values are valid and the number of values is equal to the number of column names.

        !Currently, type validation is not implemented!
        """
        required_nr_values = len(self.__column_names)
        for value in self.__values:
            if len(value) != required_nr_values:
                raise ValueError(f"Expected {required_nr_values} values, found {len(value)}.")
            # check if the types are correct

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
