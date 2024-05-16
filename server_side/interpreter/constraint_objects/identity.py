from server_side.dbmanager import DbManager
from .cobj import CObj


class Identity(CObj):
    def __init__(self, seed, increment):
        super().__init__()
        self.__seed = seed
        self.__increment = increment

    def validate(self, dbm: DbManager = None):
        """
        Check if the column already has a constraint of this type.
        Check if the seed and increment values are valid.
        """
        pass

    def get_seed(self):
        return self.__seed

    def get_increment(self):
        return self.__increment

