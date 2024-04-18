from .tobj import TObj


class TInlinePrimaryKey(TObj):
    """PRIMARY KEY"""
    def __init__(self):
        pass

    def consume(self, tokens):
        tokens.consume_concrete("primary")
        tokens.consume_concrete("key")
        self.set_length(2)
