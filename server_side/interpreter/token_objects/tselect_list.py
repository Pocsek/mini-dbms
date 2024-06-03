from server_side.interpreter.token_list import TokenList
from server_side.interpreter.token_objects.tobj import TObj


class TSelectList(TObj):
    """
    Consumes:
        <select_list>

    Syntax:
        <select_list> ::=
            {
              *
              | {
                  {
                    [ { table_name | table_alias }. ] column_name
                    | expression
                  }
                  [ [ AS ] column_alias ]
                } [ ,...n ]
            }
    """
    def __init__(self):
        pass

    def consume(self, token_list: TokenList):
        pass

    def __dict__(self):
        return []
