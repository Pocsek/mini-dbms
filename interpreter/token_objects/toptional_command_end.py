from .tobj import TObj


class TOptionalCommandEnd(TObj):
    """ ; """
    def __init__(self):
        pass

    def consume(self, tokens):
        try:
            tokens.consume_concrete(";")
        except SyntaxError:
            pass
        return tokens.get_cursor(), self
