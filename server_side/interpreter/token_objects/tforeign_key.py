from server_side.interpreter.token_objects.tobj import TObj
from server_side.interpreter.token_list import TokenList


class TForeignKey(TObj):
    """FOREIGN KEY ( SOURCE_COLUMN_REFERENCE ) REFERENCES ( TARGET_COLUMN_REFERENCE )"""
    def __init__(self):
        self.__src_col = None  # source column
        self.__ref_col = None  # reference column

    def consume(self, token_list: TokenList):
        pass

    def set_src_col(self, src_col):
        self.__src_col = src_col

    def set_ref_col(self, ref_col):
        self.__ref_col = ref_col
