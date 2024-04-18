from .custom_node import CustomNode
from .char_const import CharConst
from .inline_constraint_definitions import InlineConstraintDefinitions


class ColumnDefinition(CustomNode):
    def __init__(self, name, datatype, parent=None):
        super().__init__(parent)
        self.__name = CharConst(self, name)
        self.__datatype = CharConst(self, datatype)
        self.__constraints = InlineConstraintDefinitions(self)

    def check_validity(self):
        """
        Check if there already exists a column in the parent table with the given name.
        """
        pass

    def add_column_constraint(self, col_constr):
        col_constr.update_bpointer(self.__constraints)
