from interpreter.tree_objects.executable_tree import ExecutableTree
from interpreter.leaf_objects.char_const import CharConst


class Use(ExecutableTree):
    def __init__(self, db_name):
        super().__init__()
        self.__db_name = CharConst(db_name)

    def validate(self):
        """
        Check if a database with the given name exists.
        """
        pass

    def execute(self):
        """
        Change the working DB.
        """
        pass

    def connect_nodes_to_root(self):
        self.add_node(self.__db_name, self.root)

    def connect_subtrees_to_root(self):
        pass

    def get_name(self):
        return self.__db_name

