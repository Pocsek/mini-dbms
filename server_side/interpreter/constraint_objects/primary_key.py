from server_side.dbmanager import DbManager
from .cobj import CObj


class PrimaryKey(CObj):
    def __init__(self, column_names: list[str], constr_name=None):
        super().__init__(constr_name)
        self.__column_names = column_names

    def validate(self, dbm: DbManager = None):
        """
        Check if the columns already have a constraint of this type.
        Check if another primary key already exists in the parent table.
        """
        pass

    def get_column_names(self):
        return self.__column_names