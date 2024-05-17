from server_side.interpreter.tree_objects.executable_tree import ExecutableTree


class DropDatabase(ExecutableTree):
    """
    An ExecutableTree subclass that represents a DROP DATABASE statement.

    Syntax:
        DROP DATABASE [ IF EXISTS ] database_name [ ,...n ] [;]

    Examples:
        1. DROP TABLE table_name;
        2. DROP TABLE IF EXISTS table_name;
    """
    def __init__(self, db_names, if_exists):
        super().__init__()
        self.__db_names = db_names
        self.__if_exists = if_exists

    def _execute(self, dbm=None, mongo_client=None):
        """
        Delete the databases both through the MongoDb client and
        """
        pass

    def validate(self, dbm=None, mongo_client=None):
        """
        If the "if_exists" attribute is false, only then check if the databases exist.
        """
        pass

    def connect_nodes_to_root(self):
        pass

    def connect_subtrees_to_root(self):
        pass

