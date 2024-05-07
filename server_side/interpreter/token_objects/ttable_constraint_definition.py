from server_side.interpreter.token_objects.tobj import TObj
from server_side.interpreter.token_list import TokenList
from server_side.interpreter.token_classification import TokenType


class TTableConstraintDefinition(TObj):
    """[CONSTRAINT constraint_name] constraint_type ( constraint_args )"""
    def __init__(self):
        self.__constr_name = None
        self.__constr_type = None
        self.__src_col_name = None
        self.__ref_table_name = None
        self.__ref_col_name = None

    def consume(self, token_list: TokenList):
        match token_list.expect_type(TokenType.KEYWORD):
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
            case "on":
                pass
            case "primary":
                pass
            case "unique":
                pass
            case _:
                raise SyntaxError(f"Unexpected token at {token_list.peek()}")
