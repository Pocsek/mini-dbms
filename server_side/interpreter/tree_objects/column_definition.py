"""NOT IMPLEMENTED"""

from server_side.interpreter.tree_objects.constraint_definition import ConstraintDefinition
from server_side.interpreter.tree_objects.custom_tree import CustomTree
from server_side.interpreter.token_objects.tcolumn_definition import TColumnDefinition
from server_side.interpreter.constraint_objects import *


class ColumnDefinition(CustomTree):
    def __init__(self, tcol_def: TColumnDefinition):
        super().__init__()
        self.__name = tcol_def.get_name()
        self.__datatype = tcol_def.get_data_type()
        self.__col_constraints: list[CObj] = tcol_def.get_col_constraints()

    def validate(self, dbm=None, mongo_client=None):
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
            if isinstance(col_constraint, PrimaryKey) or isinstance(col_constraint, NotNull):
                return False
            elif isinstance(col_constraint, Null):
                return True
        return True

    def get_identity_values(self):
        for col_constraint in self.__col_constraints:
            if isinstance(col_constraint, Identity):
                return col_constraint.get_seed(), col_constraint.get_increment()
        return None, None

    def get_default_value(self):
        for col_constraint in self.__col_constraints:
            if isinstance(col_constraint, Default):
                return col_constraint.get_default_value()
        return None

    def get_check(self):
        for col_constraint in self.__col_constraints:
            if isinstance(col_constraint, Check):
                return col_constraint
        return None

    def get_keys(self):
        keys = []
        for col_constraint in self.__col_constraints:
            if isinstance(col_constraint, PrimaryKey) \
                    or isinstance(col_constraint, ForeignKey) \
                    or isinstance(col_constraint, Unique):
                keys.append(col_constraint)
        return keys
