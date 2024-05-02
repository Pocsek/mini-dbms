from treelib import Node, Tree

from .tokenizer import Tokenizer
from .token_list import TokenList
from .token_classification import TokenType, Literal

from .leaf_objects import *
from .tree_objects import *
from .token_objects import *


class Parser:
    """
    The Parser class is responsible for parsing a string of raw commands into an Abstract Syntax Tree (AST).

    The AST is a list of trees, where each tree represents a command.

    The Parser class is also responsible for validating the syntax of the commands.
    """
    def __init__(self):
        self.__ast_list = None

        self.reset_state()

    def reset_state(self):
        self.__ast_list = list()

    def get_ast_list(self):
        return self.__ast_list

    def parse(self, raw_commands):
        self.reset_state()

        tokens_all = Tokenizer.tokenize(raw_commands)
        tokens_separated = Tokenizer.extract_commands(tokens_all)
        token_lists = []
        for tokens in tokens_separated:
            token_lists.append(TokenList(tokens))

        for token_list in token_lists:
            try:
                ast = self.__parse_token_list(token_list)
                self.__ast_list.append(ast)
            except Exception:
                raise

    def __parse_token_list(self, token_list: TokenList):
        token = token_list.consume_of_type(TokenType.MAIN_KEYWORD)
        match token:
            case "use":
                return self.__parse_use(token_list)
            case "create":
                return self.__parse_create(token_list)
            case "drop":
                return self.__parse_drop(token_list)
            case "alter":
                return self.__parse_alter(token_list)
            case "insert":
                return self.__parse_insert(token_list)
            case "select":
                return self.__parse_select(token_list)
            case "update":
                return self.__parse_update(token_list)
            case "delete":
                return self.__parse_delete(token_list)
            case _:
                raise NotImplementedError(f"No implementation for '{token}''")

    def __parse_use(self, token_list: TokenList):
        db_name = token_list.consume_of_type(TokenType.IDENTIFIER)
        tree = Use(db_name)
        token_list.consume_group(TOptionalCommandEnd())
        tree.finalize()
        return tree

    def __parse_create(self, token_list: TokenList):
        token = token_list.consume_of_type(TokenType.KEYWORD)
        match token:
            case "database":
                return self.__parse_create_database(token_list)
            case "table":
                return self.__parse_create_table(token_list)
            case "index":
                return self.__parse_create_index(token_list)
            case _:
                raise SyntaxError(f"Invalid syntax at '{token}'")

    def __parse_create_database(self, token_list: TokenList):
        db_name = token_list.consume_of_type(TokenType.IDENTIFIER)
        tree = CreateDatabase(db_name)
        token_list.consume_group(TOptionalCommandEnd())
        tree.finalize()
        return tree

    def __parse_create_table(self, token_list: TokenList):
        table_name = token_list.consume_of_type(TokenType.IDENTIFIER)
        tree = CreateTable(table_name)

        token_list.consume_concrete("(")

        while token_list.has_next():
            tok_type = token_list.peek_type()
            match tok_type:
                case TokenType.IDENTIFIER:
                    tcol_def = token_list.consume_group(TColumnDefinition())
                    col_def = ColumnDefinition(tcol_def.get_name(), tcol_def.get_type(), tcol_def.get_constraints())
                    tree.add_column_definition(col_def)
                case TokenType.KEYWORD:
                    # handle constraint definition
                    pass



            # look for a column definition
            # try:
            # col_name = token_list.consume_of_type(TokenType.IDENTIFIER)
            # col_type = token_list.consume_of_type(TokenType.DATATYPE)
            # col_def = ColumnDefinition(col_name, col_type)
            #
            # constraint = None
            # if token_list.peek() not in (",", ")"):
            #     match token_list.expect_type(TokenType.KEYWORD):
            #         case "primary":
            #             token_list.consume_group(TInlinePrimaryKey())
            #             constraint = PrimaryKey()
            #         case "foreign":
            #             pass
            #     col_def.add_constraint(constraint)
            #
            #
            # # parsing was successful -> add new nodes to the tree
            # if token_list.peek() in (",", ")"):
            #     col_def.finalize()
            #     tree.add_column_definition(col_def)
            #     token_list.increment_cursor()
            # except SyntaxError:
            #     passed = False

            # look for a constraint definition
            # if not passed:
            #     token_list.consume_concrete("constraint")
            #     constr_name = token_list.consume_of_type(TokenType.IDENTIFIER)
            #     token_list.consume_of_type(TokenType.SECONDARY_KEYWORD)

            # token_list.consume(TokenType.SEPARATOR, ",")

        tree.finalize()
        print(tree)
        return tree

    def __parse_create_index(self, token_list: TokenList):
        pass

    def __parse_drop(self, token_list: TokenList):
        pass

    def __parse_alter(self, token_list: TokenList):
        pass

    def __parse_insert(self, token_list: TokenList):
        pass

    def __parse_select(self, token_list: TokenList):
        pass

    def __parse_update(self, token_list: TokenList):
        pass

    def __parse_delete(self, token_list: TokenList):
        pass


