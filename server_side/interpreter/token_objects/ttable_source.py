from server_side.interpreter.token_list import TokenList
from server_side.interpreter.token_classification import TokenType
from server_side.interpreter.token_objects.tobj import TObj
from .tselect import TSelect
from .talias import TAlias
from .tlogical_expression import TLogicalExpression


class TTableSource(TObj):
    """
    Consumes:
        <table_source>

    Syntax:
        <table_source> ::=
        {
            table_name [ [ AS ] table_alias ]
            | derived_table [ AS ] table_alias
            | <joined_table>
        }
        <joined_table> ::=
        {
            <table_source> <join_type> <table_source> ON <search_condition>
            | [ ( ] <joined_table> [ ) ]
        }
        <join_type> ::=
            [ { INNER | { { LEFT | RIGHT | FULL } [ OUTER ] } } ]
            JOIN
    """
    def __init__(self):
        self.__this = {}

    def consume(self, token_list: TokenList):
        # consume the first table source in the FROM clause
        if token_list.check_type(TokenType.IDENTIFIER):
            # table_name [ [ AS ] table_alias ]
            # database table (can migrate into a joined table further down the line)
            self.set_table_type("database")
            self.set_table_name(token_list.consume())
            if token_list.check_token("as") or token_list.check_type(TokenType.IDENTIFIER):
                self.set_table_alias(token_list.consume_group(TAlias()).get_alias())
        else:
            # derived_table [ AS ] table_alias
            token_list.consume_concrete("(")
            self.set_table_type("derived")
            self.__this["subquery"] = token_list.consume_group(TSelect(True)).__dict__()
            token_list.consume_concrete(")")
            self.set_table_alias(token_list.consume_group(TAlias()).get_alias())

        # consume table joins (INNER JOINs only)
        while True:
            # <join_type> <table_source> ON <search_condition>
            if token_list.check_token("inner"):
                token_list.consume()
                token_list.expect_concrete("join")
            if token_list.check_token("join"):
                token_list.consume()
                left_table = dict(self.__dict__())  # create a copy of this table
                self.__this = {}  # redefine this table
                self.set_table_type("joined")
                self.set_join_type("inner")
                self.set_left_table(left_table)
                self.set_right_table(token_list.consume_group(TTableSource()).__dict__())
                token_list.consume_concrete("on")
                self.set_join_condition(token_list.consume_group(TLogicalExpression()).__dict__())
            else:
                break

    def __dict__(self):
        """
        Representations:
            1) {
                "table_type": "database",
                "table_name": <table_name>,
                "table_alias": <alias>
            }

            2) {
                "table_type": "derived",
                "subquery": <query>,
                "table_alias": <alias>
            }

            3) {
                "table_type": "joined",
                "join_type": ("inner" | ...),               *only inner join is relevant for now*
                "left_table": <table_source>,               *recursive*
                "right_table": <table_source>,              *recursive*
                "join_condition": <search_condition>
            }
        """
        return self.__this

    def set_table_type(self, val: str):
        self.__this["table_type"] = val

    def set_table_name(self, val: str):
        self.__this["table_name"] = val

    def set_table_alias(self, val: str):
        self.__this["table_alias"] = val

    def set_join_type(self, val: str):
        self.__this["join_type"] = val

    def set_left_table(self, val: dict):
        self.__this["left_table"] = val

    def set_right_table(self, val: dict):
        self.__this["right_table"] = val

    def set_join_condition(self, val: dict):
        self.__this["join_condition"] = val
