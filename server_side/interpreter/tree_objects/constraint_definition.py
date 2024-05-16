"""NOT IMPLEMENTED"""

from server_side.dbmanager import DbManager
from server_side.interpreter.tree_objects.custom_tree import CustomTree
from server_side.interpreter.token_objects.tcolumn_constraint_definition import TColumnConstraintDefinition


class ConstraintDefinition(CustomTree):
    def __init__(self, tcol_constr_def: TColumnConstraintDefinition = None, ttable_constr_def = None):
        super().__init__()
        if tcol_constr_def is not None:
            self.__constr_name = tcol_constr_def.get_constraint_name()
            self.__constr_type = tcol_constr_def.get_constraint()
            self.__src_col_names = [tcol_constr_def.get_source_column_name()]
            self.__ref_table_name = tcol_constr_def.get_referenced_table_name()
            self.__ref_col_names = [tcol_constr_def.get_referenced_column_name()]
        elif ttable_constr_def is not None:
            pass
        else:
            raise ValueError("No constraint definition provided")

    def validate(self, dbm: DbManager = None, mongo_client=None):
        """
        Check if there already exists a constraint with the given name.
        Call the validate method of the constraint object (CObj).
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

    def get_constraint_name(self):
        return self.__constr_name

    def get_constraint_type(self):
        return self.__constr_type

    def get_source_column_names(self):
        return self.__src_col_names

    def get_referenced_table_name(self):
        return self.__ref_table_name

    def get_referenced_column_names(self):
        return self.__ref_col_names
