"""NOT IMPLEMENTED"""
from server_side.dbmanager import DbManager
from .cobj import CObj


class Default(CObj):
    def __init__(self, name=None):
        super().__init__(name)

    def validate(self, dbm: DbManager = None):
        pass
        """
        Check if the column already has a constraint of this type.
        Check if the given default value matches the column's datatype.
        """
        pass

