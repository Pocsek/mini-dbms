from interpreter.tree_objects.executable_tree import ExecutableTree
from interpreter.leaf_objects.char_const import CharConst


class CreateDatabase(ExecutableTree):
    def __init__(self, db_name):
        super().__init__()
        self.__db_name = CharConst(db_name)

    def validate(self):
        """
        Check if there already exists a database with the given name.
        """
        pass

    def execute(self):
        """
        Update the json structure with the new database.
        Update in MongoDB as well.
        """
        pass

    def connect_nodes_to_root(self):
        self.add_node(self.__db_name, self.root)

    def connect_subtrees_to_root(self):
        pass

    def get_name(self):
        return self.__db_name

