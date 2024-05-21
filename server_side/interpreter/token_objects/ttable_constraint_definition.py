from server_side.interpreter.token_objects.tobj import TObj
from server_side.interpreter.token_list import TokenList
from server_side.interpreter.token_classification import TokenType
from server_side.interpreter.token_objects.tvalue import TValue
from server_side.interpreter.constraint_objects import *
from server_side.interpreter.token_objects.tidentifiers import TIdentifiers
from server_side.interpreter.token_objects.toptional_on_delete_or_update import TOptionalOnDeleteOrUpdate


class TTableConstraintDefinition(TObj):
    """
    A table constraint is a constraint that can be applied to a multiple columns. It is defined after the column
    definitions.

    Syntax:
        [CONSTRAINT constraint_name] constraint_type <constraint_args>

    Example:
        CREATE TABLE t1 (
            col1 INT,
            col2 FLOAT,
            CONSTRAINT PK_t1 PRIMARY KEY (col1, col2)
        );
    """
    def __init__(self):
        self.__constraint = None
        self.__constr_name = None
        self.__src_col_names = None
        self.__ref_table_name = None
        self.__ref_col_names = None

    def consume(self, token_list: TokenList):
        match token_list.expect_type(TokenType.KEYWORD):
            case "check":
                # TODO: Implement Check class
                pass
            case "constraint":
                # CONSTRAINT constraint_name
                token_list.consume_concrete("constraint")
                self.__constr_name = token_list.consume_of_type(TokenType.IDENTIFIER)
                self.consume(token_list)  # continuation in other cases
            case "foreign":
                # FOREIGN KEY REFERENCES ref_table_name (ref_col_name)
                token_list.consume_concrete("foreign")
                token_list.consume_concrete("key")
                self.__src_col_names = token_list.consume_group(TIdentifiers()).get_identifiers()
                token_list.consume_concrete("references")
                self.__ref_table_name = token_list.consume_of_type(TokenType.IDENTIFIER)
                self.__ref_col_names = token_list.consume_group(TIdentifiers()).get_identifiers()

                on_delete = None
                on_update = None
                existsNext = True
                while existsNext:
                    on_clause = token_list.consume_group(TOptionalOnDeleteOrUpdate())
                    if not on_clause.exists():
                        existsNext = False
                    else:
                        if on_clause.get_type() == "delete":
                            on_delete = on_clause.get_action()
                        else:
                            on_update = on_clause.get_action()

                self.__constraint = ForeignKey(
                    self.__src_col_names,
                    self.__ref_table_name,
                    self.__ref_col_names,
                    on_delete,
                    on_update,
                    self.__constr_name
                )
            case "primary":
                token_list.consume_concrete("primary")
                token_list.consume_concrete("key")
                self.__ref_col_names = token_list.consume_group(TIdentifiers()).get_identifiers()
                self.__constraint = PrimaryKey(self.__ref_col_names, self.__constr_name)
            case "unique":
                token_list.consume_concrete("unique")
                self.__ref_col_names = token_list.consume_group(TIdentifiers()).get_identifiers()
                self.__constraint = Unique(self.__ref_col_names, self.__constr_name)
            case _:
                raise SyntaxError(f"Unexpected token at {token_list.peek()}")

    def get_constraint(self):
        return self.__constraint
