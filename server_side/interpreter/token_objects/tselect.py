from server_side.interpreter.token_list import TokenList
from server_side.interpreter.token_objects import (
    TObj,
    TSelectList,
    TTableSource,
    TSearchCondition,
    TGroupByExpression
)


class TSelect(TObj):
    """
    Consumes: SELECT ...

    Syntax:
        (SELECT) [DISTINCT] <select_list>
        [FROM <table_source>]
        [WHERE <search_condition>]
        [GROUP BY <group_by_expression>]
    """
    def __init__(self):
        self.__isDistinct = False
        self.__select_list = None
        self.__table_source = None
        self.__search_condition = None
        self.__group_by_expression = None

    def consume(self, token_list: TokenList):
        # token_list.consume_concrete("select")  # its already consumed in Parser.__parse_token_list()
        if token_list.check_token("distinct"):
            token_list.consume()
            self.__isDistinct = True
        self.__select_list = token_list.consume_group(TSelectList())

        if token_list.check_token("from"):
            token_list.consume()
            self.__table_source = token_list.consume_group(TTableSource())

        if token_list.check_token("where"):
            token_list.consume()
            self.__search_condition = token_list.consume_group(TSearchCondition())

        if token_list.check_token("group"):
            token_list.consume_concrete("group")
            token_list.consume_concrete("by")
            self.__group_by_expression = token_list.consume_group(TGroupByExpression())
