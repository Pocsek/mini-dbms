from server_side.interpreter.token_list import TokenList
from .tobj import TObj
from .taggregate_function import TAggregateFunction


class TFunction(TObj):
    """
    Consumes:
        <function> ::= <aggregate_function> | <date_and_time>

    Syntax:
        <aggregate_function> ::=
            COUNT([DISTINCT] <column_reference>)
            | SUM([DISTINCT] <column_reference>)
            | AVG([DISTINCT] <column_reference>)
            | MIN([DISTINCT] <column_reference>)
            | MAX([DISTINCT] <column_reference>)

        <date_and_time> ::=
            GETDATE()
    """
    def __init__(self):
        self.__type = None
        self.__function = None

    def consume(self, token_list: TokenList):
        if token_list.check_token("getdate"):
            # date & time function
            token_list.consume()
            token_list.consume_concrete("(")
            token_list.consume_concrete(")")
            self.__type = "date_and_time"
            self.__function = {"name": "getdate"}
        else:
            # aggregate function
            self.__function = token_list.consume_group(TAggregateFunction()).__dict__()
            self.__type = "aggregate"

    def __dict__(self):
        """
        Representation:
            {
                "type": ("aggregate" | "date_and_time"),
                "function": <function>
            }

        A <function> always has a "name" key.
        """
        return {
            "type": self.__type,
            "function": self.__function
        }
