from server_side.interpreter.token_list import TokenList
from server_side.interpreter.token_classification import TokenType
from server_side.interpreter.token_objects.tobj import TObj


class TColumnReference(TObj):
    """
    Consumes:
        [ { table_name | table_alias }. ] column_name
    """
    def __init__(self):
        self.__table_name = None
        self.__col_name = None

    def consume(self, token_list: TokenList):
        arg1 = token_list.consume_of_type(TokenType.IDENTIFIER)
        if token_list.check_token("."):
            token_list.consume()
            arg2 = token_list.consume_of_type(TokenType.IDENTIFIER)
            self.__table_name = arg1
            self.__col_name = arg2
        else:
            self.__col_name = arg1

    def __dict__(self):
        """
        Representation:
            {
                "table": (<table_name> | <table_alias>) (don't include if not given)
                "column": <column_name>
            }
        """
        d = {}
        if self.__table_name:
            d["table"] = self.__table_name
        d["column"] = self.__col_name
        return d

