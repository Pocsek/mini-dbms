from token_classification import TokenType
from tokenizer import Tokenizer

class TokenList:
    def __init__(self, tokens):
        self.__cursor = 0
        self.__tokens = tokens

    def __increment_cursor(self):
        self.__cursor += 1

    def has_next(self):
        return self.__cursor < len(self.__tokens)

    def peek(self):
        """Returns the token at the cursor"""
        return self.__tokens[self.__cursor]

    def consume(self, target_token_type: TokenType):
        """Returns the token at the cursor from the token list and increments the cursor if the type of the token matches the
        target token type, else raises an exception."""
        if not self.has_next():
            raise SyntaxError(f"Unexpected end of command. Expected: '{target_token_type}'")
        token = self.peek()
        token_type = Tokenizer.get_token_type(token)

        if token_type != target_token_type:
            raise SyntaxError(f"Expected: '{target_token_type}', got '{token_type}'")

        self.__increment_cursor()
        return token


