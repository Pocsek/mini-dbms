"""NOT IMPLEMENTED"""

from server_side.interpreter.tree_objects.custom_tree import CustomTree
from server_side.interpreter.leaf_objects.char_const import CharConst
from server_side.interpreter.tree_objects.inline_constraint_definitions import InlineConstraintDefinitions


class ColumnDefinition(CustomTree):
    def __init__(self, name, datatype, constraints: InlineConstraintDefinitions = None):
        super().__init__()
        self.__name = CharConst(name)
        self.__datatype = CharConst(datatype)
        self.__constraints = InlineConstraintDefinitions() if None else constraints

        self.finalize()

    def validate(self):
        """
        Check if there already exists a column in the parent table with the given name.
        """
        pass

    def connect_nodes_to_root(self) -> None:
        self.add_node(self.__name, self.root)
        self.add_node(self.__datatype, self.root)

    def connect_subtrees_to_root(self):
        self.paste(self.root, self.__constraints)

    def add_constraint(self, constraint):
        self.__constraints.add_node(constraint, self.__constraints.root)
        # self.__constraints.paste(self.__constraints.root, constraint)

    def get_constraints(self):
        return self.__constraints
