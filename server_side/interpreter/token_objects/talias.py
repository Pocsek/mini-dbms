from server_side.interpreter.token_list import TokenList
from server_side.interpreter.token_classification import TokenType
from server_side.interpreter.token_objects.tobj import TObj


class TAlias(TObj):
    """
    Consumes:
        [ AS ] alias
    """
    def __init__(self):
        self.__alias = None

    def consume(self, token_list: TokenList):
        if token_list.check_token("as"):
            token_list.consume()
        self.__alias = token_list.consume_of_type(TokenType.IDENTIFIER)

    def get_alias(self):
        return self.__alias
