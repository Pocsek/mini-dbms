"""NOT IMPLEMENTED"""

from server_side.dbmanager import DbManager
from server_side.interpreter.tree_objects.custom_tree import CustomTree
from server_side.interpreter.token_objects.tcolumn_constraint_definition import TColumnConstraintDefinition
from server_side.interpreter.constraint_objects import *


class ConstraintDefinition(CustomTree):
    def __init__(self, tcol_constr_def: TColumnConstraintDefinition = None):
        super().__init__()
        if tcol_constr_def is not None:
            self.__constr_name = tcol_constr_def.get_constraint_name()
            self.__constr_type = tcol_constr_def.get_constraint_type()
            self.__src_col_name = tcol_constr_def.get_source_column_name()
            self.__ref_table_name = tcol_constr_def.get_referenced_table_name()
            self.__ref_col_names = [tcol_constr_def.get_referenced_column_name()]

    def validate(self, dbm: DbManager = None, mongo_client=None):
        """
        Check if there already exists a column in the parent table with the given name.
        """
        pass

    def connect_nodes_to_root(self) -> None:
        pass

    def connect_subtrees_to_root(self):
        pass

    def get_name(self):
        return self.__name

    def get_datatype(self):
        return self.__datatype

    def get_col_constraints(self):
        return self.__col_constraints

    def is_allow_nulls(self):
        for col_constraint in self.__col_constraints:
            if isinstance(col_constraint, Null):
                return True
            elif isinstance(col_constraint, NotNull):
                return False
        return True

    def get_identity_values(self):
        for col_constraint in self.__col_constraints:
            if isinstance(col_constraint, Identity):
                return col_constraint.get_seed(), col_constraint.get_increment()
        return None, None

    def get_constraint_name(self):
        return self.__constr_name

    def get_constraint_type(self):
        return self.__constr_type

    def get_source_column_name(self):
        return self.__src_col_name

    def get_referenced_table_name(self):
        return self.__ref_table_name

    def get_referenced_column_names(self):
        return self.__ref_col_names
