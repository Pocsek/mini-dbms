from interpreter.tree_objects.custom_tree import CustomTree
from interpreter.node_objects.column_definitions import ColumnDefinitions
from interpreter.node_objects.char_const import CharConst
from interpreter.node_objects.table_level_constraint_definitions import TableLevelConstraintDefinitions


class CreateTable(CustomTree):
    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.__name = CharConst(tree_id=self, value=name)
        self.__col_defs = ColumnDefinitions(tree_id=self)
        self.__constr_defs = TableLevelConstraintDefinitions(tree_id=self)

        self.add_node(self.__name, self.root)
        self.add_node(self.__col_defs, self.root)
        self.add_node(self.__constr_defs, self.root)

    def check_validity(self):
        """
        Check if there already exists a table with the given name.
        """
        pass

    def get_name(self):
        return self.__name

    def get_column_definitions(self):
        return self.__col_defs

    def get_constraint_definitions(self):
        return self.__constr_defs

    def add_column_definition(self, col_def):
        self.add_node(col_def, self.__col_defs)

    def add_constraint_definition(self, constr_def):
        self.add_node(constr_def, self.__constr_defs)
