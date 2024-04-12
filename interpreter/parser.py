from treelib import Node, Tree

from tokenizer import Tokenizer
from token_list import TokenList
from token_classification import TokenType, Literal


class ASTNode:
    """Node of an Abstract Syntax Tree"""
    def __init__(self, token_type, value=None):
        self.token_type = token_type
        self.value = value


class Parser:
    @classmethod
    def parse(cls, raw_commands):
        tokens_all = Tokenizer.tokenize(raw_commands)
        tokens_separated = Tokenizer.extract_commands(tokens_all)
        token_lists = []
        for tokens in tokens_separated:
            token_lists.append(TokenList(tokens))

        ast_list = []  # list of abstract syntax trees
        for token_list in token_lists:
            try:
                ast = parse_token_list(token_list)
                ast_list.append(ast)
            except Exception:
                raise

        return ast_list


def parse_token_list(token_list: TokenList):
    token = token_list.get_next()
    token_type = Tokenizer.get_token_type(token)

    match token_type:
        case "use":
            return parse_use(token_list)
        case "create":
            return parse_create(token_list)
        case "drop":
            return parse_drop(token_list)
        case "alter":
            return parse_alter(token_list)
        case "insert":
            return parse_insert(token_list)
        case "select":
            return parse_select(token_list)
        case "update":
            return parse_delete(token_list)
        case "delete":
            return parse_delete(token_list)
        case _:
            raise SyntaxError(f"Expected: '{TokenType.MAIN_KEYWORD}', got '{token_type}'")


def parse_use(token_list: TokenList):
    pass


def parse_create(token_list: TokenList):
    token = token_list.get_next()
    if token is None:
        raise SyntaxError(f"Unexpected end of command: after '{token}'")
    token_type = Tokenizer.get_token_type(token)
    match token_type:
        case "database":
            return parse_create_database(token_list)
        case "table":
            return parse_create_table(token_list)
        case "index":
            return parse_create_index(token_list)
        case _:
            raise SyntaxError(f"Expected: '{TokenType.SECONDARY_KEYWORD}', got '{token_type}'")


def parse_create_database(token_list: TokenList):
    pass


def parse_create_table(token_list: TokenList):
    ast = Tree()
    ast.create_node("create_table", 0, data=ASTNode(TokenType.MAIN_KEYWORD))
    # ...
    # ...


def parse_create_index(token_list: TokenList):
    pass


def parse_drop(token_list: TokenList):
    pass


def parse_alter(token_list: TokenList):
    pass


def parse_insert(token_list: TokenList):
    pass


def parse_select(token_list: TokenList):
    pass


def parse_update(token_list: TokenList):
    pass


def parse_delete(token_list: TokenList):
    pass
