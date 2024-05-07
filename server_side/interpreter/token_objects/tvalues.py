from .tobj import TObj
from server_side.interpreter.token_classification import TokenType
from server_side.interpreter.token_list import TokenList
from server_side.interpreter.tokenizer import Tokenizer


class TValues(TObj):
    """
    Consumes a list of values between parentheses. Includes the parentheses.
    """

    def __init__(self):
        self.__values = []

    def consume(self, token_list: TokenList):
        token_list.consume_concrete("(")
        while token_list.has_next():
            value = token_list.peek()
            if self.__is_value(value):
                token_list.increment_cursor()
                self.__values.append(value)
            else:
                raise SyntaxError(f"Unexpected token at {value}")
            if token_list.has_next():
                next_token = token_list.peek()
                if next_token == ")":
                    token_list.consume_concrete(")")
                    break
                if next_token == ",":
                    token_list.consume_concrete(",")
            else:
                raise SyntaxError("Unexpected end of command. Expected ')' or ','")
        self.set_length(len(self.__values) + 2)
        return token_list.get_cursor(), self

    def get_length(self):
        return super().get_length()

    def set_length(self, value):
        super().set_length(value)

    def get_values(self):
        return self.__values

    def __is_value(self, token):
        """
        Returns True if the token is either a number or a character constant.
        """
        return Tokenizer.get_token_type(token) in (TokenType.NUM_CONST, TokenType.CHAR_CONST)
