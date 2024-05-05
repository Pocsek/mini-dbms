from .tobj import TObj
from .tinline_primary_key import TInlinePrimaryKey

from ..token_classification import TokenType
from ..leaf_objects import PrimaryKey


class TColumnDefinition(TObj):
    """<column_name> <data_type> [ <column_constraint> [,... n] ]"""
    def __init__(self):
        self.__col_name = None
        self.__data_type = None
        self.__col_constraints = []

    def consume(self, tokens):
        self.__col_name = tokens.consume_of_type(TokenType.IDENTIFIER)
        self.__data_type = tokens.consume_of_type(TokenType.DATATYPE)

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
            self.__col_constraints.append(constraint)

        tokens.increment_cursor()

    def get_name(self):
        return self.__col_name

    def get_data_type(self):
        return self.__data_type

    def get_constraints(self):
        return self.__col_constraints
