from treelib import Node, Tree

from .tokenizer import Tokenizer
from .token_list import TokenList
from .token_classification import TokenType, Literal

from .leaf_objects import *
from .tree_objects import *
from .token_objects import *


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
                ast = cls.__parse_token_list(token_list)
                ast_list.append(ast)
            except Exception:
                raise

        return ast_list

    @classmethod
    def __parse_token_list(cls, token_list: TokenList):
        token = token_list.consume_of_type(TokenType.MAIN_KEYWORD)
        match token:
            case "use":
                return cls.__parse_use(token_list)
            case "create":
                return cls.__parse_create(token_list)
            case "drop":
                return cls.__parse_drop(token_list)
            case "alter":
                return cls.__parse_alter(token_list)
            case "insert":
                return cls.__parse_insert(token_list)
            case "select":
                return cls.__parse_select(token_list)
            case "update":
                return cls.__parse_update(token_list)
            case "delete":
                return cls.__parse_delete(token_list)
            case _:
                raise NotImplementedError(f"No implementation for '{token}''")

    @classmethod
    def __parse_use(cls, token_list: TokenList):
        db_name = token_list.consume_of_type(TokenType.IDENTIFIER)
        tree = Use(db_name)
        token_list.consume_group(TOptionalCommandEnd())
        tree.finalize()
        return tree

    @classmethod
    def __parse_create(cls, token_list: TokenList):
        token = token_list.consume_of_type(TokenType.KEYWORD)
        match token:
            case "database":
                return cls.__parse_create_database(token_list)
            case "table":
                return cls.__parse_create_table(token_list)
            case "index":
                return cls.__parse_create_index(token_list)
            case _:
                raise SyntaxError(f"Invalid syntax at '{token}'")

    @classmethod
    def __parse_create_database(cls, token_list: TokenList):
        db_name = token_list.consume_of_type(TokenType.IDENTIFIER)
        tree = CreateDatabase(db_name)
        token_list.consume_group(TOptionalCommandEnd())
        tree.finalize()
        return tree

    @classmethod
    def __parse_create_table(cls, token_list: TokenList):
        table_name = token_list.consume_of_type(TokenType.IDENTIFIER)
        tree = CreateTable(table_name)

        token_list.consume_concrete("(")

        while token_list.has_next():
            if token_list.peek_type() == TokenType.IDENTIFIER:
                tcol_def = token_list.consume_group(TColumnDefinition())
                col_def = ColumnDefinition(tcol_def.get_name(), tcol_def.get_type(), tcol_def.get_constraints())
                tree.add_column_definition(col_def)


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

    @classmethod
    def __parse_create_index(cls, token_list: TokenList):
        pass

    @classmethod
    def __parse_drop(cls, token_list: TokenList):
        pass

    @classmethod
    def __parse_alter(cls, token_list: TokenList):
        pass

    @classmethod
    def __parse_insert(cls, token_list: TokenList):
        pass

    @classmethod
    def __parse_select(cls, token_list: TokenList):
        pass

    @classmethod
    def __parse_update(cls, token_list: TokenList):
        pass

    @classmethod
    def __parse_delete(cls, token_list: TokenList):
        pass
