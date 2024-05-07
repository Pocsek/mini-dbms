"""NOT IMPLEMENTED"""
from server_side.dbmanager import DbManager
from .cobj import CObj


class ForeignKey(CObj):
    def __init__(self, name=None):
        super().__init__(name)

    def validate(self, dbm: DbManager = None):
        """
        Check if the column already has a constraint of this type.
        Check whether the referenced table exists.
        Check whether the referenced column exists.
        Check whether the referenced column is a primary key or has a unique constraint on it.
        """
        pass
