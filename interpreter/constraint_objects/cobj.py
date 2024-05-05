from abc import ABC, abstractmethod
from dbmanager import DbManager


class CObj(ABC):
    def __init__(self, constr_name=None):
        super().__init__()
        self.__constr_name = constr_name

    @abstractmethod
    def validate(self, dbm: DbManager = None):
        pass

    def get_constraint_name(self):
        return self.__constr_name

