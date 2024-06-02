from server_side.interpreter.token_list import TokenList
from server_side.interpreter.token_objects.tobj import TObj


class TTableSource(TObj):
    """
    Consumes:
        <table_source>

    Syntax:
        <table_source> ::=
        {
            table_name [ [ AS ] table_alias ]
            | derived_table [ [ AS ] table_alias ] [ ( column_alias [ , ...n ] ) ]
            | <joined_table>
        }
        <joined_table> ::=
        {
            <table_source> <join_type> <table_source> ON <search_condition>
            | <table_source> CROSS JOIN <table_source>
            | [ ( ] <joined_table> [ ) ]
        }
        <join_type> ::=
            [ { INNER | { { LEFT | RIGHT | FULL } [ OUTER ] } } ]
            JOIN
        <column_list> ::=
            column_name [ , ...n ]
    """
    def __init__(self):
        pass

    def consume(self, token_list: TokenList):
        pass
