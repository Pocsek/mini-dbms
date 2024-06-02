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
        dropped_table_names: list[str] = []
        for table_name in self.__table_names:
            if table_name not in [tb.get_name() for tb in db.get_tables()] and self.__if_exists:
                continue
            dbm.drop_table(table_name)
            dropped_table_names.append(table_name)
        resp_message = f"Table(s) [{' ,'.join(dropped_table_names)}] dropped successfully."
        self.get_result().set_response_message(resp_message)
        print(resp_message)

    def validate(self, dbm, **kwargs):
        """
        Check integrity violations.

        If the "if_exists" attribute is false, only then check if the tables exist in the working database inside the
        json structure.
        :param **kwargs:
        """
        # TODO: Check integrity violations.

        if self.__if_exists:
            return
        db = dbm.get_working_db()
        for table_name in self.__table_names:
            if table_name not in [tb.get_name() for tb in db.get_tables()]:
                raise ValueError(f"Table '{table_name}' does not exist")

    def connect_nodes_to_root(self):
        pass

    def connect_subtrees_to_root(self):
        pass

