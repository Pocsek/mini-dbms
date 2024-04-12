class TokenList:
    def __init__(self, tokens):
        self.__cursor = -1
        self.__tokens = tokens

    def has_next(self):
        return self.__cursor + 1 < len(self.__tokens)

    def get_next(self):
        self.__cursor += 1
        if self.has_next():
            return self.__tokens[self.__cursor]
        return None
