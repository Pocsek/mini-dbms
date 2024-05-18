# from .cobj import CObj
# from .primary_key import PrimaryKey
from server_side.interpreter.constraint_objects import *


class Null(CObj):
    def __init__(self, col_name):
        super().__init__()
        self.__col_name = col_name

    def validate(self, dbm, **kwargs):
        """
        Check if the column already has a NULL constraint.
        Check if the column has a NOT NULL constraint.
        Check if the column is a primary key.
        """
        column_definition = kwargs.get("column_definition")
        if not column_definition:
            raise ValueError("Column definition not given in NULL constraint validation.")
        # TODO column_definition.validate_has_constraint_not_more_than_once(Null.__name__)
        # TODO if column_definition.has_constraint(NotNull.__name__):
        #     raise ValueError(
        #         f"Column '{self.__col_name}': cannot have both NULL and NOT NULL constraints on the same column."
        #     )
        # TODO if column_definition.has_constraint(PrimaryKey.__name__):
        #     raise ValueError(
        #         f"Column '{self.__col_name}': cannot have a NULL constraint on a primary key."
        #     )

    def get_column_name(self):
        return self.__col_name

