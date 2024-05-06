from server_side.interpreter.tree_objects.executable_tree import ExecutableTree
from server_side.interpreter.leaf_objects.char_const import CharConst
from server_side.dbmanager import DbManager
from server_side.database_objects import Database


class CreateDatabase(ExecutableTree):
    def __init__(self, db_name):
        super().__init__()
        self.__db_name = CharConst(db_name)

    def validate(self, dbm: DbManager = None, mongo_client=None):
        """
        Check if there already exists a database with the given name.
        """
        pass

    def _execute(self, dbm: DbManager = None, mongo_client=None):
        """
        Update the json structure with the new database.
        """
        new_db = Database(self.__db_name.get_value())
        dbm.add_database(new_db)
        dbm.update_databases()

    def connect_nodes_to_root(self):
        self.add_node(self.__db_name, self.root)

    def connect_subtrees_to_root(self):
        pass

    def get_name(self):
        return self.__db_name

