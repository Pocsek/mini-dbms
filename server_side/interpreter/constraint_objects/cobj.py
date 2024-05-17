from abc import ABC, abstractmethod


class CObj(ABC):
    def __init__(self, constr_name=None):
        super().__init__()
        self.__constr_name = constr_name

    @abstractmethod
    def validate(self, dbm):
        """
        :param dbm: DbManager instance
        """
        pass

    def get_constraint_name(self):
        return self.__constr_name

