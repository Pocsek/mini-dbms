from server_side.interpreter.token_classification import TokenType
from server_side.interpreter.tokenizer import Tokenizer


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

    def check_token(self, target_token):
        """Returns True if the token at the cursor matches the target token, else False."""
        if not self.has_next():
            return False
        return self.peek() == target_token

    def check_type(self, target_token_type: TokenType):
        """Returns True if the type of the token at the cursor matches the target type, else False."""
        if not self.has_next():
            return False
        return self.peek_type() == target_token_type

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

    def consume(self):
        """Simply returns the token at the cursor from the token list and increments the cursor."""
        if not self.has_next():
            raise SyntaxError(f"Unexpected end of command")
        token = self.peek()
        self.increment_cursor()
        return token

    def consume_concrete(self, target_token):
        """
        Returns the target token and increments the cursor if the target token matches the token at the cursor,
        else raises an exception.
        """
        if not self.has_next():
            raise SyntaxError(f"Unexpected end of command. Expected '{target_token}'")

        self.expect_concrete(target_token)
        self.increment_cursor()
        return target_token

    def consume_group(self, consumer):
        """
        Process a group of tokens defined by a TObj.
        :param consumer: a subclass of TObj
        :return: the modified consumer
        """
        consumer.consume(self)
        return consumer

    def consume_either(self, target_token_list):
        """
        Attempts to consume a token from the token list. If the token is not in the target token list, raises an
        exception.
        :return: the consumed token (if successful)
        """
        cur_token = ""
        for target_token in target_token_list:
            cur_token = self.peek()
            if cur_token == target_token:
                self.increment_cursor()
                return cur_token
        raise SyntaxError(f"Expected one of {target_token_list}, found {cur_token}")
