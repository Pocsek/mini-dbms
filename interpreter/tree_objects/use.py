from interpreter.tree_objects.custom_tree import CustomTree
from interpreter.leaf_objects.char_const import CharConst


class Use(CustomTree):
    def __init__(self, db_name):
        super().__init__()
        self.__db_name = CharConst(db_name)

    def check_validity(self) -> None:
        """
        Check if there exists a database with the given name.
        """
        pass

    def connect_nodes_to_root(self) -> None:
        self.add_node(self.__db_name, self.root)

    def connect_subtrees_to_root(self) -> None:
        pass

    def get_name(self):
        return self.__db_name

