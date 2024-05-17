from .cobj import CObj


class Default(CObj):
    def __init__(self, default_value, constr_name=None):
        super().__init__(constr_name)
        self.__default_value = default_value

    def validate(self, dbm):
        pass
        """
        Check if the column already has a constraint of this type.
        Check if the given default value matches the column's datatype.
        """
        pass

    def get_default_value(self):
        return self.__default_value
