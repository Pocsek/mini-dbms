# from .cobj import CObj
from server_side.interpreter.constraint_objects import *


class Default(CObj):
    def __init__(self, col_name, default_value, constr_name=None):
        super().__init__(constr_name)
        self.__col_name = col_name
        self.__default_value = default_value

    def validate(self, dbm, **kwargs):
        """
        Check if the column already has a constraint of this type.
        Check if the given default value matches the column's datatype.
        """
        column_definition = kwargs.get("column_definition")
        if not column_definition:
            raise ValueError("Column definition not given in DEFAULT constraint validation.")
        # TODO column_definition.validate_has_constraint_not_more_than_once(Default.__name__)

        col_dtype = column_definition.get_datatype()
        matching = True
        match col_dtype:
            case "int":
                if not isinstance(self.__default_value, int):
                    matching = False
            case "float":
                if not isinstance(self.__default_value, float):
                    matching = False
            case "str":
                if not isinstance(self.__default_value, str):
                    matching = False
            case "bool":
                if not isinstance(self.__default_value, bool):
                    matching = False
            case _:
                raise ValueError(f"Unknown datatype '{col_dtype}'.")
        if not matching:
            raise ValueError(f"Default value '{self.__default_value}' does not match column's datatype.")

    def get_column_name(self):
        return self.__col_name

    def get_default_value(self):
        return self.__default_value
