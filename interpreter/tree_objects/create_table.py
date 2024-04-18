from treelib import Tree

from interpreter.tree_objects.custom_tree import CustomTree
from interpreter.tree_objects.column_definitions import ColumnDefinitions
from interpreter.leaf_objects.char_const import CharConst
from interpreter.tree_objects.table_level_constraint_definitions import TableLevelConstraintDefinitions


class CreateTable(CustomTree):
    def __init__(self, name):
        super().__init__()
        self.__name = CharConst(name)
        self.__col_defs = ColumnDefinitions()
        self.__constr_defs = TableLevelConstraintDefinitions()

        # self.connect_nodes_to_root()
        # self.connect_subtrees_to_root()

    def check_validity(self) -> None:
        """
        Check if there already exists a table with the given name.
        """
        pass

    def connect_nodes_to_root(self) -> None:
        self.add_node(self.__name, self.root)

    def connect_subtrees_to_root(self) -> None:
        self.paste(self.root, self.__col_defs)
        self.paste(self.root, self.__constr_defs)

    def get_name(self):
        return self.__name

    def get_column_definitions(self):
        return self.__col_defs

    def get_constraint_definitions(self):
        return self.__constr_defs

    def add_column_definition(self, col_def):
        self.__col_defs.paste(self.__col_defs.root, col_def)

    def add_constraint_definition(self, constr_def):
        self.__constr_defs.paste(self.__constr_defs_defs.root, constr_def)
