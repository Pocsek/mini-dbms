from server_side.interpreter.token_objects.tobj import TObj


class TInlinePrimaryKey(TObj):
    """PRIMARY KEY"""
    def __init__(self):
        pass

    def consume(self, tokens):
        tokens.consume_concrete("primary")
        tokens.consume_concrete("key")
