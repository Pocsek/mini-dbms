from server_side.interpreter.tree_objects.executable_tree import ExecutableTree


class DropDatabase(ExecutableTree):
    """
    An ExecutableTree subclass that represents a DROP DATABASE statement.

    Syntax:
        DROP DATABASE [ IF EXISTS ] database_name [ ,...n ] [;]
    """
    def __init__(self, db_names, if_exists):
        super().__init__()
        self.__db_names = db_names
        self.__if_exists = if_exists

    def _execute(self, dbm):
        """
        Delete the databases in MongoDB and update the databases.json structure.
        If the "if_exists" attribute is true, only try to delete the databases that exist.
        """
        dropped_db_names: list[str] = []
        for db_name in self.__db_names:
            if dbm.find_database(db_name) == -1 and self.__if_exists:
                continue
            dbm.drop_database(db_name)
            dropped_db_names.append(db_name)
        resp_message = f"Database(s) [{' ,'.join(dropped_db_names)}] dropped successfully."
        self.get_result().set_response_message(resp_message)
        print(resp_message)

    def validate(self, dbm, **kwargs):
        """
        If the "if_exists" attribute is false, only then check if the databases exist in the json structure.
        """
        for db_name in self.__db_names:
            if db_name == dbm.get_working_db().get_name():
                raise ValueError(f"Cannot drop '{db_name}' because it is the working database")
            if db_name in dbm.get_default_database_names():
                raise ValueError(f"Database '{db_name}' is a default database and cannot be dropped")
            if not self.__if_exists:
                if dbm.find_database(db_name) == -1:
                    raise ValueError(f"Database '{db_name}' does not exist")

    def connect_nodes_to_root(self):
        pass

    def connect_subtrees_to_root(self):
        pass

