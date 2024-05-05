"""NOT IMPLEMENTED"""
from dbmanager import DbManager
from .custom_tree import CustomTree
from ..token_objects.tcolumn_definition import TColumnDefinition


class ColumnDefinition(CustomTree):
    def __init__(self, tcol_def: TColumnDefinition):
        super().__init__()
        self.__name = tcol_def.get_name()
        self.__datatype = tcol_def.get_data_type()
        self.__col_constraints = tcol_def.get_col_constraints()  # a list of Constraint objects

    def validate(self, dbm: DbManager = None, mongo_client=None):
        """
        Check if there already exists a column in the parent table with the given name.
        """
        pass

    def connect_nodes_to_root(self) -> None:
        pass

    def connect_subtrees_to_root(self):
        pass
