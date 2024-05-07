from server_side.interpreter.token_objects.tobj import TObj
from server_side.interpreter.token_objects.tinline_primary_key import TInlinePrimaryKey

from server_side.interpreter.token_classification import TokenType
from server_side.interpreter.leaf_objects import PrimaryKey


class TColumnDefinition(TObj):
    """COL_NAME COL_TYPE [CONSTRAINTS]"""
    def __init__(self):
        self.__col_name = None
        self.__col_type = None
        self.__constraints = []

    def get_name(self):
        return self.__col_name

    def get_type(self):
        return self.__col_type

    def get_constraints(self):
        return self.__constraints

    def consume(self, tokens):
        self.__col_name = tokens.consume_of_type(TokenType.IDENTIFIER)
        self.__col_type = tokens.consume_of_type(TokenType.DATATYPE)

        while tokens.peek() not in (",", ")"):
            constraint = None
            match tokens.expect_type(TokenType.KEYWORD):
                case "check":
                    pass
                case "constraint":
                    pass
                case "default":
                    pass
                case "foreign":
                    pass
                case "not":
                    pass
                case "null":
                    pass
                case "primary":
                    tokens.consume_group(TInlinePrimaryKey())
                    constraint = PrimaryKey()
                case "unique":
                    pass
                case _:
                    raise SyntaxError(f"Unexpected token at {tokens.peek()}")
            self.__constraints.append(constraint)

        tokens.increment_cursor()

        return tokens.get_cursor(), self
