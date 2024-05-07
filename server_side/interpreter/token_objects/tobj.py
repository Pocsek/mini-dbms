from abc import ABC, abstractmethod
from server_side.interpreter.token_list import TokenList


class TObj(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def consume(self, token_list: TokenList):
        """
        Consumes tokens from the token list (TokenList) and sets the object's attributes.
        :return: None
        """
        pass
