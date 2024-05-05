"""NOT IMPLEMENTED"""
from dbmanager import DbManager
from .cobj import CObj


class Check(CObj):
    def __init__(self, constr_name=None):
        super().__init__(constr_name)

    def validate(self, dbm: DbManager = None):
        """
        Check if the column already has a constraint of this type.
        """
        pass



