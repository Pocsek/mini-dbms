from server_side.interpreter.token_list import TokenList
from .tobj import TObj
from .tcolumn_reference import TColumnReference


class TAggregateFunction(TObj):
    """
    Consumes:
        <aggregate_function>

    Syntax:
        <aggregate_function> ::=
            COUNT([DISTINCT] <column_reference>)
            | SUM([DISTINCT] <column_reference>)
            | AVG([DISTINCT] <column_reference>)
            | MIN([DISTINCT] <column_reference>)
            | MAX([DISTINCT] <column_reference>)
    """
    def __init__(self):
        self.__is_distinct = False
        self.__name = None
        self.__column_reference = None

    def consume(self, token_list: TokenList):
        self.__name = token_list.consume_either(["count", "sum", "avg", "min", "max"])
        token_list.consume_concrete("(")
        if token_list.check_token("distinct"):
            token_list.consume()
            self.__is_distinct = True
        self.__column_reference = token_list.consume_group(TColumnReference()).__dict__()
        token_list.consume_concrete(")")

    def __dict__(self):
        """
        Representation:
            {
                "is_distinct": True | False,
                "name": ("count" | "sum" | "avg" | "min" | "max"),
                "column_reference": <column_reference>
            }
        """
        return {
            "is_distinct": self.__is_distinct,
            "name": self.__name,
            "column_reference": self.__column_reference
        }
