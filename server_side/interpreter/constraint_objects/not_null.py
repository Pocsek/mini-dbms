# from .cobj import CObj
from server_side.interpreter.constraint_objects import *


class NotNull(CObj):
    def __init__(self, col_name):
        super().__init__()
        self.__col_name = col_name

    def validate(self, dbm, **kwargs):
        """
        Check if the column already has a NOT NULL constraint.
        Check if the column has a NULL constraint.
        """
        column_definition = kwargs.get("column_definition")
        if not column_definition:
            raise ValueError("Column definition not given in NOT NULL constraint validation.")
        column_definition.validate_has_constraint_not_more_than_once(NotNull.__name__)
        if column_definition.has_constraint(Null.__name__):
            raise ValueError(
                f"Column '{self.__col_name}': cannot have both a NULL constraint and a NOT NULL constraint on the "
                f"same column."
            )

    def get_column_name(self):
        return self.__col_name

