from server_side.interpreter.tree_objects.executable_tree import ExecutableTree


class DropTable(ExecutableTree):
    """
    An ExecutableTree subclass that represents a DROP TABLE statement.

    Syntax:
        DROP TABLE [ IF EXISTS ] table_name [ ,...n ] [;]
    """
    def __init__(self, table_names, if_exists):
        super().__init__()
        self.__table_names = table_names
        self.__if_exists = if_exists

    def _execute(self, dbm):
        """
        Delete the tables in the working database and update the databases.json structure.
        If the "if_exists" attribute is true, only try to delete the tables that exist.
        """
        db = dbm.get_working_db()
        for table_name in self.__table_names:
            if table_name not in [tb.get_name() for tb in db.get_tables()] and self.__if_exists:
                continue
            dbm.drop_table(table_name)
            print(f"Table '{table_name}' dropped successfully.")

    def validate(self, dbm, **kwargs):
        """
        If the "if_exists" attribute is false, only then check if the tables exist in the working database inside the
        json structure.

        Check integrity violations: if the table is referenced by a foreign key, i.e. it's a parent table, then reject
        the operation.
        """
        db = dbm.get_working_db()
        for table_name in self.__table_names:
            if not self.__if_exists:
                if table_name not in [tb.get_name() for tb in db.get_tables()]:
                    raise ValueError(f"Table '{table_name}' does not exist")
            self.__validate_has_no_child_table(db, table_name)

    def __validate_has_no_child_table(self, db, to_delete_table_name):
        for other_table in db.get_tables():
            for fk in other_table.get_foreign_keys():
                if fk.get_referenced_table_name() == to_delete_table_name:
                    raise ValueError(f"Cannot drop table '{to_delete_table_name}' because it is referenced by "
                                     f"'{other_table.get_name()}'")

    def connect_nodes_to_root(self):
        pass

    def connect_subtrees_to_root(self):
        pass

