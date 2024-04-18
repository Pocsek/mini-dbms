from abc import ABC, abstractmethod
from ..token_list import TokenList


class TObj(ABC):
    __length = 0  # the number of tokens the object consists of

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def consume(self, token_list: TokenList):
        pass

    def get_length(self):
        return self.__length

    def set_length(self, value):
        self.__length = value

