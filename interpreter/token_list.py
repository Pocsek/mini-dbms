from .token_classification import TokenType
from .tokenizer import Tokenizer


class TokenList:
    def __init__(self, tokens):
        self.__cursor = 0
        self.__tokens = tokens

    def get_cursor(self):
        return self.__cursor

    def increment_cursor(self):
        self.__cursor += 1

    def has_next(self):
        return self.__cursor < len(self.__tokens)

    def peek(self):
        """Returns the token at the cursor without moving the cursor."""
        if not self.has_next():
            raise IndexError("Cursor out of bounds.")
        return self.__tokens[self.__cursor]

    def peek_type(self):
        """Returns the type of the token at the cursor"""
        return Tokenizer.get_token_type(self.peek())

    def expect_type(self, target_token_type: TokenType):
        """Same as 'consume_of_type' but without incrementing the cursor."""
        if not self.has_next():
            raise SyntaxError(f"Unexpected end of command. Expected type '{target_token_type}'")
        token = self.peek()
        token_type = Tokenizer.get_token_type(token)

        if token_type != target_token_type:
            raise SyntaxError(f"Expected type '{target_token_type}', found '{token_type}' at '{token}'")

        return token

    def consume_of_type(self, target_token_type: TokenType):
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

        self.increment_cursor()
        return token

    def expect_concrete(self, target_token):
        """Raises an exception if the current token does not match the target token."""
        token = self.peek()
        if token != target_token:
            raise SyntaxError(f"Expected token '{target_token}', found '{token}'")

    def consume_concrete(self, target_token):
        """
        Returns the token at the cursor from the token list and increments the cursor if the token matches the
        target token, else raises an exception.
        """
        if not self.has_next():
            raise SyntaxError(f"Unexpected end of command. Expected '{target_token}'")

        self.expect_concrete(target_token)
        self.increment_cursor()

    def consume_group(self, consumer):
        """
        Process a given type of token and move the cursor the needed amount.
        :param consumer: a token to be consumed (a token object instance)
        :return: <the new position of the cursor>, <an object of the same type as 'consumer' with its fields set
        respectively>
        """
        consumer.consume(self)
        return consumer




