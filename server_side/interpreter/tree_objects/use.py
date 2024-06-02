from server_side.interpreter.tree_objects.executable_tree import ExecutableTree
from server_side.interpreter.leaf_objects.char_const import CharConst


class Use(ExecutableTree):
    def __init__(self, db_name):
        super().__init__()
        self.__db_name = CharConst(db_name)

    def validate(self, dbm, **kwargs):
        """
        Check if a database with the given name exists.
        """
        if dbm.find_database(self.__db_name.get_value()) == -1:
            raise ValueError(f"Database '{self.__db_name.get_value()}' does not exist.")

    def _execute(self, dbm):
        """
        Change the working DB.
        """
        dbm.set_working_db_index(dbm.find_database(self.__db_name.get_value()))
        resp_message = f"Changed database context to '{self.__db_name.get_value()}'."
        self.get_result().set_response_message(resp_message)
        print(resp_message)

    def connect_nodes_to_root(self):
        self.add_node(self.__db_name, self.root)

    def connect_subtrees_to_root(self):
        pass

    def get_name(self):
        return self.__db_name

