from server_side.interpreter.tokenizer import Tokenizer
from server_side.interpreter.token_list import TokenList

from server_side.interpreter.tree_objects import (
    Use,
    CreateDatabase,
    CreateTable,
    CreateIndex,
    DropDatabase,
    DropTable,
    InsertInto,
    DeleteFrom,
    ColumnDefinition,
    Select
)
from server_side.interpreter.token_objects import (
    TOptionalCommandEnd,
    TColumnDefinition,
    TTableConstraintDefinition,
    TIdentifiers,
    TValues,
    TSelect
)
from server_side.interpreter.token_classification import TokenType


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
            ast = self.__parse_token_list(token_list)
            self.__ast_list.append(ast)

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
        return tree

    def __parse_create_table(self, token_list: TokenList):
        tree = CreateTable()

        table_name = token_list.consume_of_type(TokenType.IDENTIFIER)
        tree.set_name(table_name)

        token_list.consume_concrete("(")
        while token_list.has_next():
            tok_type = token_list.peek_type()
            match tok_type:
                case TokenType.IDENTIFIER:
                    # A column definition is expected
                    tcol_def = token_list.consume_group(TColumnDefinition())
                    tree.add_column_definition(ColumnDefinition(tcol_def))
                case TokenType.KEYWORD:
                    # A table constraint definition is expected
                    tconstr_def = token_list.consume_group(TTableConstraintDefinition())
                    tree.add_table_constraint(tconstr_def.get_constraint())
                case _:
                    # end of definition or end of command expected
                    t = token_list.consume_either([",", ")"])
                    if t == ")":
                        token_list.consume_group(TOptionalCommandEnd())

        return tree

    def __parse_create_index(self, token_list: TokenList):
        "CREATE INDEX index_name ON table_name (column1, column2, ...);"
        index_name = token_list.consume_of_type(TokenType.IDENTIFIER)
        token_list.consume_concrete('on')
        table_name = token_list.consume_of_type(TokenType.IDENTIFIER)
        tok_idents: TIdentifiers = token_list.consume_group(TIdentifiers())
        column_names: list = tok_idents.get_identifiers()

        tree = CreateIndex()
        tree.set_index_name(index_name)
        tree.set_table_name(table_name)
        tree.set_column_names(column_names)
        return tree


    def __parse_drop(self, token_list: TokenList):
        token = token_list.consume_of_type(TokenType.KEYWORD)
        match token:
            case "database":
                return self.__parse_drop_database(token_list)
            case "table":
                return self.__parse_drop_table(token_list)
            case _:
                raise SyntaxError(f"Invalid syntax at '{token}'")

    def __parse_drop_database(self, token_list: TokenList):
        if_exists = False
        if token_list.peek_type() == TokenType.KEYWORD:
            token_list.consume_concrete("if")
            token_list.consume_concrete("exists")
            if_exists = True

        db_names = []
        while token_list.has_next():
            db_name = token_list.consume_of_type(TokenType.IDENTIFIER)
            db_names.append(db_name)
            try:
                token_list.consume_concrete(",")
            except:
                token_list.consume_group(TOptionalCommandEnd())

        tree = DropDatabase(db_names, if_exists)
        return tree

    def __parse_drop_table(self, token_list: TokenList):
        if_exists = False
        if token_list.peek_type() == TokenType.KEYWORD:
            token_list.consume_concrete("if")
            token_list.consume_concrete("exists")
            if_exists = True

        table_names = []
        while token_list.has_next():
            table_name = token_list.consume_of_type(TokenType.IDENTIFIER)
            table_names.append(table_name)
            try:
                token_list.consume_concrete(",")
            except:
                token_list.consume_group(TOptionalCommandEnd())

        tree = DropTable(table_names, if_exists)
        return tree

    def __parse_alter(self, token_list: TokenList):
        pass

    def __parse_insert(self, token_list: TokenList):
        # Example use:
        # insert into table_name (col1, col2, col3) values (val1, val2, val3), (val4, val5, val6)
        tree = InsertInto()  # create the tree
        token_list.consume_concrete("into")
        table_name = token_list.consume_of_type(TokenType.IDENTIFIER)
        tree.set_table_name(str(table_name))  # add the table name to the tree
        if token_list.has_next():
            if token_list.peek_type() == TokenType.PARENTHESIS:
                # if the column names are specified
                tidents: TIdentifiers = token_list.consume_group(TIdentifiers())
                for ident in tidents.get_identifiers():  # add the column names to the tree if they are specified
                    tree.add_column_name(str(ident))
            else:
                # if the column names are not specified
                pass
            # parse the values
            token_list.consume_concrete("values")
            list_of_tvalues: list[TValues] = []
            while token_list.has_next():  # while there is a ',' continue reading tvalues
                tvals: TValues = token_list.consume_group(TValues())
                list_of_tvalues.append(tvals)
                if token_list.has_next():
                    next_token = token_list.peek()
                    if next_token == ",":
                        token_list.consume_concrete(",")
                    else:
                        break
            for tvals in list_of_tvalues:  # add the values to the tree
                tree.add_value([str(val) for val in tvals.get_values()])

        else:
            raise SyntaxError("Unexpected end of command. Expected '(' or 'values'.")
        return tree

    def __parse_select(self, token_list: TokenList):
        tree = Select(token_list.consume_group(TSelect(consume_select_keyword=False)))
        return tree

    def __parse_update(self, token_list: TokenList):
        pass

    def __parse_delete(self, token_list: TokenList):
        # Example use: delete from table_name where condition
        token_list.consume_concrete("from")  # consume the 'from' keyword
        table_name = token_list.consume_of_type(TokenType.IDENTIFIER)
        token_list.consume_concrete("where")
        column_name = token_list.consume_of_type(TokenType.IDENTIFIER)
        token_list.consume_concrete("=")
        tok_type = token_list.peek_type()
        value = token_list.peek()
        if tok_type == TokenType.NUM_CONST:
            value = token_list.consume_of_type(TokenType.NUM_CONST)
        elif tok_type == TokenType.CHAR_CONST:
            value = token_list.consume_of_type(TokenType.CHAR_CONST)
        else:
            raise SyntaxError(f"Unexpected token at {value}")

        tree = DeleteFrom()
        tree.set_table_name(str(table_name))
        tree.set_condition({str(column_name): value})
        return tree


