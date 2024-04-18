from .tobj import TObj
from ..token_list import TokenList


class TIdentity(TObj):
    """IDENTITY[(seed, increment)]"""
    def __init__(self):
        self.__seed = None
        self.__increment = None

    def consume(self, token_list: TokenList):
        pass

    def set_seed(self, value):
        self.__seed = value

    def set_increment(self, value):
        self.__increment = value
