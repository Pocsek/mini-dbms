# from .cobj import CObj
from server_side.interpreter.constraint_objects import *


class Identity(CObj):
    def __init__(self, seed, increment, col_name):
        super().__init__()
        self.__seed = seed
        self.__increment = increment
        self.__col_name = col_name

    def validate(self, dbm, **kwargs):
        """
        Check if the column already has a constraint of this type.
        Assure that not other column has identity constraint, as only one column can have identity constraint per table.
        Check if the seed and increment values are valid.
        """
        column_definition = kwargs.get("column_definition")
        if not column_definition:
            raise ValueError("Column definition not given in IDENTITY constraint validation.")
        # TODO column_definition.validate_has_constraint_not_more_than_once(Identity.__name__)

        column_definitions = kwargs.get("column_definitions")
        if not column_definitions:
            raise ValueError(f"Column definitions not given in IDENTITY constraint validation.")
        # TODO for col_def in column_definitions:
        #     if col_def == column_definition:  # exclude self from the list
        #         continue
        #     if col_def.has_constraint(Identity.__name__):
        #         raise ValueError(f"Column '{column_definition.get_name()}': cannot have more than one IDENTITY "
        #                          f"constraints on the same table.")

        if not isinstance(self.__seed, int):
            raise ValueError(f"Column '{column_definition.get_name()}': seed must be an integer.")
        if not isinstance(self.__increment, int):
            raise ValueError(f"Column '{column_definition.get_name()}': increment must be an integer.")
        if self.__seed < 0:
            raise ValueError(f"Column '{column_definition.get_name()}': seed must be a positive number.")
        if self.__increment < 0:
            raise ValueError(f"Column '{column_definition.get_name()}': increment must be a positive number.")

    def get_seed(self):
        return self.__seed

    def get_increment(self):
        return self.__increment

    def get_col_name(self):
        return self.__col_name
