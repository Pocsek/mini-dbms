from server_side.interpreter.token_objects.tobj import TObj
from server_side.interpreter.token_list import TokenList


class TTableLevelPrimaryKey(TObj):
    """PRIMARY KEY ( COLUMN_REFERENCE1, [COLUMN_REFERENCE2], ... )"""
    def __init__(self):
        self.__ref_cols = None  # reference columns

    def consume(self, token_list: TokenList):
        pass

    def set_ref_cols(self, ref_cols):
        self.__ref_cols = ref_cols
