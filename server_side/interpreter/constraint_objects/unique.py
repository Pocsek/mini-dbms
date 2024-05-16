from server_side.dbmanager import DbManager
from .cobj import CObj


class Unique(CObj):
    def __init__(self, col_names, constr_name=None):
        super().__init__(constr_name)
        self.__col_names = col_names

    def validate(self, dbm: DbManager = None):
        """
        Check if the column already has a constraint of this type.
        """
        pass

    def get_column_names(self):
        return self.__col_names
