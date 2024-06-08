from server_side.interpreter.token_list import TokenList
from server_side.interpreter.token_objects.tobj import TObj


class TGroupByExpression(TObj):
    """"""
    def __init__(self):
        self.__column_references = []

    def consume(self, token_list: TokenList):
        from .tcolumn_reference import TColumnReference
        while token_list.has_next():
            col_ref = token_list.consume_group(TColumnReference()).__dict__()
            self.__column_references.append(col_ref)
            if token_list.check_token(","):
                token_list.consume()
            else:
                break

    def get_column_references(self):
        return self.__column_references
