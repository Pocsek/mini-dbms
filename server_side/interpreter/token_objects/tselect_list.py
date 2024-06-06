from server_side.interpreter.token_list import TokenList
from server_side.interpreter.token_classification import TokenType
from .tobj import TObj
from .tcolumn_reference import TColumnReference
from .talias import TAlias


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
        self.__selections = []

    def consume(self, token_list: TokenList):
        if token_list.check_token("*"):
            token_list.consume()
            self.__selections.append({"type": "*"})
            token_list.expect_concrete("from")
            return

        while True:
            selection = {}
            if token_list.check_type(TokenType.IDENTIFIER):
                # [ { table_name | table_alias }. ] column_name
                selection["type"] = "column"
                column_reference = token_list.consume_group(TColumnReference()).__dict__()
                selection["column_reference"] = column_reference
            else:
                # expression
                selection["type"] = "expression"
                from .tvalue_expression import TValueExpression
                selection["value"] = token_list.consume_group(TValueExpression()).__dict__()
            if token_list.check_token("as"):
                # [ [ AS ] column_alias ]
                alias = token_list.consume_group(TAlias()).get_alias()
                selection["alias"] = alias
            self.__selections.append(selection)

            if token_list.check_token(","):
                token_list.consume()
            else:
                break

    def __dict__(self):
        """
        Returns a list of dicts, each dict representing a column selection.

        Column selection representations:
            1) {
                "type": "*"
                }
            }
            2) {
                "type": "column"
                "column_reference": <column_reference>
                "alias": <column_alias> (don't include if not given)
            }
            3) {
                "type": "expression"
                "value": <value_expression>
                "alias": <column_alias> (don't include if not given)
            }
        """
        return self.__selections
