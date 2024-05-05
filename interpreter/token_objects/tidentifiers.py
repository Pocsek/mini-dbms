from .tobj import TObj
from ..token_classification import TokenType
from ..token_list import TokenList


class TIdentifiers(TObj):
    """
    Consumes a list of identifiers between parentheses. Includes the parentheses.
    """

    def __init__(self):
        self.__identifiers = []

    def consume(self, token_list: TokenList):
        token_list.consume_concrete("(")
        while token_list.has_next():
            identifier = token_list.consume_of_type(TokenType.IDENTIFIER)
            self.__identifiers.append(identifier)
            if token_list.has_next():
                next_token = token_list.peek()
                if next_token == ")":
                    token_list.consume_concrete(")")
                    break
                if next_token == ",":
                    token_list.consume_concrete(",")
            else:
                raise SyntaxError("Unexpected end of command. Expected ')' or ','")
        self.set_length(len(self.__identifiers) + 2)  # +2 for the parentheses
        return token_list.get_cursor(), self

    def get_length(self):
        return super().get_length()

    def set_length(self, value):
        super().set_length(value)

    def get_identifiers(self):
        return self.__identifiers
