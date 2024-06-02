from server_side.interpreter.tree_objects.executable_tree import ExecutableTree


class DeleteFrom(ExecutableTree):
    """
    Represents a DELETE FROM command.
    Only works with the primary key. And only if the primary key is a single column.
    Examples:
        DELETE FROM table_name WHERE primary_key = value
    """

    def __init__(self):
        super().__init__()
        self.__table_name: str = ""
        self.__condition: dict = {}  # the condition given in the where clause interpreted as a dictionary

    def _execute(self, dbm):
        db_idx = dbm.get_working_db_index()
        table_idx = dbm.find_table(db_idx, self.__table_name)
        db = dbm.get_working_db()
        table = db.get_tables()[table_idx]
        pr = table.get_primary_key()
        key = self.__make_key(pr.get_column_names(), self.__condition)
        del_count = dbm.delete(db, table, key)
        self.get_result().set_nr_rows_affected(del_count)

    def validate(self, dbm, **kwargs):
        """
        Checks if the table exists in the database.
        Checks if the condition refers to existing columns.
        Checks if the condition refers to only the primary key.

        !In the future might want to validate the condition too!
        """
        db_idx = dbm.get_working_db_index()
        tb_idx = dbm.find_table(db_idx, self.__table_name)
        if tb_idx == -1:
            raise ValueError(f"Table [{self.__table_name}] does not exist in the database.")
        tb = dbm.get_working_db().get_tables()[tb_idx]
        # check if the condition refers to existing columns
        existing_column_names = dbm.get_column_names(db_idx, tb_idx)
        for col in self.__condition.keys():
            if col not in existing_column_names:
                raise ValueError(f"Column [{col}] does not exist in the table [{self.__table_name}].")
        # check if the condition refers to only the primary key
        pr = tb.get_primary_key()
        if not pr:
            raise ValueError(f"Table [{self.__table_name}] has no primary key.")
        pr_column_names = pr.get_column_names()
        for col in self.__condition.keys():
            if col not in pr_column_names:
                raise ValueError(f"Column [{col}] is not part of the primary key of the table [{self.__table_name}].")
        # validate deletion from parent table
        self.__validate_foreign_keys(dbm)

    def connect_nodes_to_root(self):
        pass

    def connect_subtrees_to_root(self):
        pass

    def set_table_name(self, table_name: str):
        self.__table_name = table_name

    def get_table_name(self) -> str:
        return self.__table_name

    def set_condition(self, condition: dict):
        self.__condition = condition

    def get_condition(self) -> dict:
        return self.__condition

    def __make_key(self, primary_key_columns: list[str], condition: dict) -> str:
        """
        Concatenates the values of the primary key columns in the condition to make a key.
        Separator character is "#".
        """
        key = ""
        for col in primary_key_columns:
            key += condition[col] + "#"
        return key[:-1]  # leave out the last separator character

    def __validate_foreign_keys(self, dbm):
        """
        Find all child tables and check if the value being deleted exists in any of the child tables.
        """
        db = dbm.get_working_db()
        for table in db.get_tables():
            for fk in table.get_foreign_keys():
                if fk.get_referenced_table_name() == self.__table_name:
                    self.__validate_foreign_key(dbm, db, db.get_table(self.__table_name), table, fk)

    def __validate_foreign_key(self, dbm, db, parent_table, child_table, foreign_key):
        """
        Check if the value being deleted exists in the child table
        """
        db_name = db.get_name()
        chlid_table_name = child_table.get_name()
        child_col_names = foreign_key.get_source_column_names()
        values_to_delete = list(self.__condition.values())

        ok = True
        # if the foreign key being deleted is a primary key, then search by primary key
        if child_table.is_primary_key(child_col_names):
            if dbm.find_by_primary_key(db_name, chlid_table_name, values_to_delete):
                ok = False
        # else search by value
        else:
            if dbm.find_by_value(db_name, chlid_table_name, child_col_names, values_to_delete):
                ok = False
        if not ok:
            raise ValueError(f"Cannot delete value from parent table [{parent_table.get_name()}] because it exists "
                             f"in child table [{chlid_table_name}].")
