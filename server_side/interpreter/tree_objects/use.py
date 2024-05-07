from server_side.interpreter.tree_objects.executable_tree import ExecutableTree
from server_side.interpreter.leaf_objects.char_const import CharConst
from server_side.dbmanager import DbManager


class Use(ExecutableTree):
    def __init__(self, db_name):
        super().__init__()
        self.__db_name = CharConst(db_name)

    def validate(self, dbm: DbManager = None, mongo_client=None):
        """
        Check if a database with the given name exists.
        """
        pass

    def _execute(self, dbm: DbManager = None, mongo_client=None):
        """
        Change the working DB.
        """
        dbm.set_working_db_index(dbm.find_database(self.__db_name.get_value()))
        print(f"Changed database context to '{dbm.get_working_db().get_name()}'.")

    def connect_nodes_to_root(self):
        self.add_node(self.__db_name, self.root)

    def connect_subtrees_to_root(self):
        pass

    def get_name(self):
        return self.__db_name

