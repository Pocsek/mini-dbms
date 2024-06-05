from server_side.interpreter.token_objects.tobj import TObj
from server_side.interpreter.token_classification import TokenType
from server_side.interpreter.token_list import TokenList


class TValue(TObj):
    """
    Consumes a number or a string.
    """
    def __init__(self):
        self.__value = None

    def consume(self, token_list: TokenList):
        next_type = token_list.peek_type()
        if next_type == TokenType.NUM_CONST:
            self.__value = int(token_list.peek())
        # TODO: handle float numbers too
        elif next_type == TokenType.CHAR_CONST:
            self.__value = token_list.peek()
        else:
            raise SyntaxError(f"Expected a number or a string at '{token_list.peek()}'")
        token_list.increment_cursor()

    def get_value(self):
        return self.__value
