# from .cobj import CObj
from server_side.interpreter.constraint_objects import *


class PrimaryKey(CObj):
    def __init__(self, column_names: list[str], constr_name=None):
        super().__init__(constr_name)
        self.__column_names = column_names

    def validate(self, dbm, **kwargs):
        """
        If the constraint is defined inside a column definition:
            - Check if the column already has a primary key constraint.
            - Check if another column has a primary key constraint.
            - Check inside the table constraints for primary key constraints.

        Else (the constraint is defined as a table constraint):
            - Check for other primary key constraints in the table constraints.
            - Check if the referenced column names are valid.

        In all cases:
            - Check if any of the primary key columns have a null constraint.
        """
        column_definitions = kwargs.get("column_definitions")
        if not column_definitions:
            raise ValueError(f"Column definitions not given in PRIMARY KEY constraint validation.")

        table_constraints = kwargs.get("table_constraints")
        if not table_constraints:
            raise ValueError(f"Table constraints not given in PRIMARY KEY constraint validation.")


        column_definition = kwargs.get("column_definition")
        if column_definition:  # the constraint is defined inside a column definition
            # TODO column_definition.validate_has_constraint_not_more_than_once(PrimaryKey.__name__)

            # TODO for col_def in column_definitions:
            #     if col_def == column_definition:  # exclude self from the list
            #         continue:
            #     if col_def.has_constraint(PrimaryKey.__name__):
            #         raise ValueError(f"Column '{column_definition.get_name()}': cannot have more than one PRIMARY KEY "
            #                          f"constraints on the same table.")

            for constr in table_constraints:
                if isinstance(constr, PrimaryKey):
                    raise ValueError(f"Column '{column_definition.get_name()}': cannot have more than one PRIMARY KEY "
                                     f"constraints on the same table.")
        else:  # the constraint is a table constraint
            for constr in table_constraints:
                if constr == self:  # exclude self from the list
                    continue
                if isinstance(constr, PrimaryKey):
                    raise ValueError(f"Table '{kwargs.get('table_name')}': cannot have more than one PRIMARY KEY "
                                     f"constraints on the same table.")

            for col_name in self.__column_names:
                found = False
                for col_def in column_definitions:
                    if col_def.get_name() == col_name:
                        # TODO if col_def.has_constraint(Null.__name__):
                        #     raise ValueError(f"Column '{col_name}': cannot be part of a PRIMARY KEY constraint "
                        #                      f"if it has a NULL constraint.")
                        found = True
                        break
                if not found:
                    raise ValueError(f"Invalid PRIMARY KEY column reference: '{col_name}'.")

    def get_column_names(self):
        return self.__column_names
