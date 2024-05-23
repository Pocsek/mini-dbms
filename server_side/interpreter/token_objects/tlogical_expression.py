from server_side.interpreter.token_objects.tobj import TObj
from server_side.interpreter.token_classification import TokenType
from server_side.interpreter.token_list import TokenList
from server_side.interpreter.token_objects.tvalue import TValue


class TLogicalExpression(TObj):
    """
    Consumes a logical expression which is usually followed by a WHERE clause.

    This version only considers the AND operator between two expressions, i.e. the OR operator is not handled.
    Thus, we won't store what operator is in between two expressions, because we know it can only be AND.
    The result object will be a list of expressions, where an expression stores:
        1. what is on its left side
        2. the operator
        3. what is on its right side.

    Does not consume any parentheses. This is a no parentheses version.

    Input examples:
        1. col1 > 5
        2. col1 = col3 AND 0 < col2 AND 1 != 2

    Output examples in JSON (outputs for the inputs above):
        1.  [
                {
                  "left": col1,
                  "op": ">",
                  "right": 5
                }
            ]
        2.  [
                {
                  "left": col1,
                  "op": "=",
                  "right": col3
                },
                {
                  "left": 0,
                  "op": "<",
                  "right": col2
                }
                {
                  "left": 1,
                  "op": "!=",
                  "right": 2
                }
            ]

    """
    def __init__(self):
        self.__expressions: list[dict] = []

    def consume(self, token_list: TokenList):
        while token_list.has_next():
            if token_list.peek_type() == TokenType.IDENTIFIER:
                left = token_list.consume_of_type(TokenType.IDENTIFIER)
            else:
                left = token_list.consume_group(TValue()).get_value()
            op = token_list.consume_of_type(TokenType.LOGICAL_OPERATOR)
            if token_list.peek_type() == TokenType.IDENTIFIER:
                right = token_list.consume_of_type(TokenType.IDENTIFIER)
            else:
                right = token_list.consume_group(TValue()).get_value()
            self.__expressions.append({
                "left": left,
                "op": op,
                "right": right
            })

            if token_list.has_next():
                token_list.consume_concrete("and")

    def get_expressions(self):
        return self.__expressions
