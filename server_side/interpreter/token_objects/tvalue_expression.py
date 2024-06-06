from server_side.interpreter.token_objects.tobj import TObj
from server_side.interpreter.token_classification import TokenType
from server_side.interpreter.token_list import TokenList
from .tfunction import TFunction


class TValueExpression(TObj):
    """
    Consumes:
        <value_expression> ::= <constant> | <aggregate_function> | <subquery>
    """
    def __init__(self):
        self.__value = None
        self.__type = None

    def consume(self, token_list: TokenList):
        match token_list.peek_type():
            # numeric constant
            case TokenType.NUM_CONST:
                self.__type = "constant"
                self.__value = token_list.consume()
                if token_list.check_type(TokenType.BINARY_OPERATOR):
                    raise NotImplementedError("Numeric operations inside expressions are not supported yet")

            # character constant
            case TokenType.CHAR_CONST:
                self.__type = "constant"
                self.__value = token_list.consume()
                if token_list.check_type(TokenType.BINARY_OPERATOR):
                    raise NotImplementedError("String operations inside expressions are not supported yet")

            # function
            case TokenType.KEYWORD:
                self.__type = "function"
                self.__value = token_list.consume_group(TFunction()).__dict__()

            # subquery
            case TokenType.PARENTHESIS:
                token_list.consume_concrete("(")
                from .tselect import TSelect
                self.__type = "subquery"
                self.__value = token_list.consume_group(TSelect(True))
                token_list.consume_concrete(")")

    def __dict__(self):
        """
        Representation:
            {
                "type": ("constant" | "aggregate" | "subquery"),
                "value": <constant> | <aggregate_function> | <subquery>
            }
        """
        return {
            "type": self.__type,
            "value": self.__value
        }
