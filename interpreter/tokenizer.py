import sqlparse
import re

from .token_classification import *


class Tokenizer:
    @classmethod
    # takes a string of SQL commands and turns it into a list of strings where each keyword, operator, separator, etc. is a
    # different list element -> this is an essential step to take before starting to interpret the commands
    def tokenize(cls, commands_string) -> list[str]:
        tokenized = re.sub(r"([(),;])", r" \1 ", commands_string)  # put space around parentheses, separators
        tokenized = sqlparse.format(
            tokenized,
            keyword_case="lower", # cast keywords to lowercase (create, select, group by, or, between, etc. EXCLUDING DATATYPES like int, float, etc.)
            strip_comments=True  # remove comments (both "--" and "/* */" variants)
        )
        tokenized = re.sub(r"(>=|<=|<>|!=|\+=|-=|\*=|/=|%=)", r" \1 ", tokenized)  # put space around compound operators
        tokenized = re.sub(r"([^><+\-*/%=])(>|<|[+\-*/%@=])([^=])", r"\1 \2 \3", tokenized)  # put space around simple operators
        tokenized = tokenized.replace("\n", " ")  # concatenate all lines into one line
        tokenized = re.sub(" +", " ", tokenized)  # remove extra spaces
        tokenized = tokenized.strip()  # remove possible trailing space
        tokenized = tokenized.split(" ")  # split by spaces

        # cast datatypes to lowercase
        for i, val in enumerate(tokenized):
            val_lower = val.lower()
            if val_lower in Literal.DATATYPES:
                tokenized[i] = val_lower

        return tokenized

    @classmethod
    def extract_commands(cls, tokens) -> list[list[str]]:
        # separates commands based on main_commands
        # a command is a list of tokens
        # returns a list of commands
        commands: list[list[str]] = []
        c_idx: int = 0  # current command start index
        while True:
            if c_idx >= len(tokens):
                # no more tokens
                break
            if tokens[c_idx] not in Literal.MAIN_KEYWORDS:
                # command not found on current index
                print(f"Command not found: {tokens[c_idx]}")
                return []
            # next command index is either the end of tokens or the next command index
            next_c_idx = next_index_of_command(c_idx, tokens)

            command: list[str] = tokens[c_idx:next_c_idx]
            commands.append(command)
            c_idx = next_c_idx

        return commands

    @classmethod
    def get_token_type(cls, token):
        if token in Literal.MAIN_KEYWORDS:
            return TokenType.MAIN_KEYWORD
        if token in Literal.OTHER_KEYWORDS:
            return TokenType.OTHER_KEYWORD
        if token in Literal.DATATYPES:
            return TokenType.DATATYPE
        if token in Literal.PARENTHESES:
            return TokenType.PARENTHESIS
        if token in Literal.SEPARATORS:
            return TokenType.SEPARATOR
        if token in Literal.UNARY_OPERATORS:
            return TokenType.UNARY_OPERATOR
        if token in Literal.BINARY_OPERATORS:
            return TokenType.BINARY_OPERATOR
        if token.isdigit():
            return TokenType.NUM_CONST
        if token.startswith("\"") or token.startswith("'") or token.endswith("\"") or token.endswith("'"):
            return TokenType.CHAR_CONST
        return TokenType.IDENTIFIER


def first_index_of_command(li: list[str]) -> int:
    # find the index of the first main_command (keyword) in the list
    # return -1 if no main_command is found
    for (idx, token) in enumerate(li):
        if token in Literal.MAIN_KEYWORDS:
            return idx
    return -1


def next_index_of_command(start_c_idx, tokens):
    # find the index of the next main_command in the list which is not in brackets
    next_c_idx: int = len(tokens)  # next command index set to end of tokens if no more commands
    last_idx: int = start_c_idx  # last command index set to the start command index
    while True:
        # find the next command index not in brackets if it exists
        current_idx: int = first_index_of_command(tokens[last_idx + 1:])
        if current_idx == -1:
            # no more commands
            break
        current_idx += last_idx + 1  # adjust index to the original list
        if not bracket_started(tokens[start_c_idx + 1:current_idx]):
            # if the next command is not in brackets
            # checks brackets from the first command (NOT from the last) to the current
            next_c_idx = current_idx
            break
        else:
            # if the next command is in brackets
            last_idx = current_idx
    return next_c_idx


def bracket_started(li: list[str]) -> bool:
    # check if a bracket has started but not closed
    bracket_count = 0
    for token in li:
        if token == "(":
            bracket_count += 1
        elif token == ")":
            bracket_count -= 1
            if bracket_count < 0:
                # closing bracket before opening bracket
                return False
    return bracket_count > 0
