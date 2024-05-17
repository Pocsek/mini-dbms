from .cobj import CObj


class Null(CObj):
    def __init__(self, col_name):
        super().__init__()
        self.__col_name = col_name

    def validate(self, dbm):
        """
        Check if the column already has a NULL constraint.
        Assure that the column is not a primary key.
        """
        pass

    def get_column_name(self):
        return self.__col_name

