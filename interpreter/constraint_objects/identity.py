"""NOT IMPLEMENTED"""
from dbmanager import DbManager
from .cobj import CObj


class Identity(CObj):
    def __init__(self, name=None):
        super().__init__(name)

    def validate(self, dbm: DbManager = None):
        """
        Check if the column already has a constraint of this type.
        Check if the seed and increment values are valid.
        """
        pass

