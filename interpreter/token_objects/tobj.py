from abc import ABC, abstractmethod
from ..token_list import TokenList


class TObj(ABC):
    __length = 0  # !!! Unnecessary, should be deleted !!!

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def consume(self, token_list: TokenList):
        """
        Consumes tokens from the token list and sets the object's attributes.
        :return: None
        """
        pass

    def get_length(self):
        """ !!! Unnecessary, should be deleted !!! """
        return self.__length

    def set_length(self, value):
        """ !!! Unnecessary, should be deleted !!! """
        self.__length = value

