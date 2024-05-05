"""NOT IMPLEMENTED"""
from dbmanager import DbManager
from .custom_tree import CustomTree
from .column_constraint_definition import ColumnConstraintDefinition


class ColumnDefinition(CustomTree):
    def __init__(self, name, datatype, col_constraints=None):
        super().__init__()
        self.__name = ""
        self.__datatype = ""
        self.__col_constraints = []

        self.finalize()

    def validate(self, dbm: DbManager = None, mongo_client=None):
        """
        Check if there already exists a column in the parent table with the given name.
        """
        pass

    def connect_nodes_to_root(self) -> None:
        self.add_node(self.__name, self.root)
        self.add_node(self.__datatype, self.root)

    def connect_subtrees_to_root(self):
        self.paste(self.root, self.__col_constraints)

    def add_constraint(self, constraint):
        self.__col_constraints.add_node(constraint, self.__col_constraints.root)
        # self.__constraints.paste(self.__constraints.root, constraint)

    def get_constraints(self):
        return self.__col_constraints
