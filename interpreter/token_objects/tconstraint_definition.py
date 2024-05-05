from .tobj import TObj
from ..token_list import TokenList


class TConstraintDefinition(TObj):
    """[CONSTRAINT constraint_name] constraint_type ( constraint_args )"""
    def __init__(self):
        self.__constraint_name = None
        self.__constraint_type = None
        # self.__

    def consume(self, token_list: TokenList):
        pass
