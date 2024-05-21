from .cobj import CObj


class Check(CObj):
    def __init__(self, column_name, op, value, constr_name=None):
        super().__init__(constr_name)
        self.__column_name = column_name
        self.__op = op
        self.__value = value

    def validate(self, dbm, **kwargs):
        """
        Check if the column already has a constraint of this type.
        """
        pass

    def get_column_name(self):
        return self.__column_name

    def get_op(self):
        return self.__op

    def get_value(self):
        return self.__value



