"""NOT IMPLEMENTED"""
from server_side.interpreter.token_objects.tobj import TObj
from server_side.interpreter.token_classification import TokenType
from server_side.interpreter.token_list import TokenList


class TLogicalExpression(TObj):
    """
    Consumes a logical expression that has a true/false outcome.
    A logical expression can consist of:
        - numbers
        - column references
        - comparison operators

    Examples:
        1. (col1 > 5)
        2. (col1 = 5 AND col2 < 10)
    """
    def __init__(self):
        pass

    def consume(self, token_list: TokenList):
        pass
