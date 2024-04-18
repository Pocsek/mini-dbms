from .token_classification import TokenType
from .tokenizer import Tokenizer


class TokenList:
    def __init__(self, tokens):
        self.__cursor = 0
        self.__tokens = tokens

    def increment_cursor(self):
        self.__cursor += 1

    def has_next(self):
        return self.__cursor < len(self.__tokens)

    def peek(self):
        """Returns the token at the cursor"""
        return self.__tokens[self.__cursor]

    def consume(self, target_token_type: TokenType, concrete_value=None):
        """
        Returns the token at the cursor from the token list and increments the cursor if the token matches the
        target token, else raises an exception.
        """
        if not self.has_next():
            raise SyntaxError(f"Unexpected end of command. Expected type '{target_token_type}'")
        token = self.peek()
        token_type = Tokenizer.get_token_type(token)

        if token_type != target_token_type:
            raise SyntaxError(f"Expected type '{target_token_type}', found '{token_type}' at '{token}'")

        if concrete_value is not None and token != concrete_value:
            raise SyntaxError(f"Expected token '{concrete_value}', found '{token}'")

        self.increment_cursor()
        return token


