from server_side.interpreter.token_list import TokenList
from .tobj import TObj


class TSelect(TObj):
    """
    Consumes:
        <query>

    Syntax:
        <query> ::=
            SELECT [DISTINCT] <select_list>
            [FROM <table_source>]
            [WHERE <search_condition>]
            [GROUP BY <group_by_expression>]

    :param consume_select_keyword: Whether to consume the "SELECT" keyword or not.
    """
    def __init__(self, consume_select_keyword: bool):
        self.__consume_select_keyword = consume_select_keyword

        self.__is_distinct = False
        self.__select_list = None
        self.__table_source = None
        self.__search_condition = None
        self.__group_by_expression = None

    def consume(self, token_list: TokenList):
        from .tselect_list import TSelectList
        from .ttable_source import TTableSource
        from .tlogical_expression import TLogicalExpression
        from .tgroup_by_expression import TGroupByExpression

        if self.__consume_select_keyword:
            token_list.consume_concrete("select")

        if token_list.check_token("distinct"):
            token_list.consume()
            self.__is_distinct = True
        self.__select_list = token_list.consume_group(TSelectList())

        if token_list.check_token("from"):
            token_list.consume()
            self.__table_source = token_list.consume_group(TTableSource())

        if token_list.check_token("where"):
            token_list.consume()
            self.__search_condition = token_list.consume_group(TLogicalExpression())

        if token_list.check_token("group"):
            token_list.consume_concrete("group")
            token_list.consume_concrete("by")
            self.__group_by_expression = token_list.consume_group(TGroupByExpression()).get_column_references()

    def __dict__(self):
        """
        Representation:
            {
                "is_distinct": True | False,
                "select_list": <select_list> [,]
                ["table_source": <table_source> [,] ]
                ["search_condition": <search_condition> [,] ]
                ["group_by_expression": <group_by_expression> [,] ]
            }
        """

        # default arguments that must be available
        d = {
            "is_distinct": self.__is_distinct,
            "select_list": self.__select_list.__dict__()
        }

        # optional arguments
        if self.__table_source:
            d["table_source"] = self.__table_source.__dict__()
        if self.__search_condition:
            d["search_condition"] = self.__search_condition.__dict__()
        if self.__group_by_expression:
            d["group_by_expression"] = self.__group_by_expression
        return d
