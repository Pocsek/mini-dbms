from server_side.interpreter.token_objects.tobj import TObj
from server_side.interpreter.token_objects.tidentifiers import TIdentifiers
from server_side.interpreter.token_objects.toptional_on_delete_or_update import TOptionalOnDeleteOrUpdate
from server_side.interpreter.token_list import TokenList
from server_side.interpreter.token_classification import TokenType
from server_side.interpreter.token_objects.tlogical_expression import TLogicalExpression
from server_side.interpreter.token_objects.tvalue import TValue
from server_side.interpreter.constraint_objects import *


class TColumnConstraintDefinition(TObj):
    """[CONSTRAINT constraint_name] constraint_type ( constraint_args )"""
    def __init__(self, src_col_name=None):
        self.__constr_name = None
        self.__constr_type: CObj | None = None
        self.__src_col_name = src_col_name if src_col_name is not None else None
        self.__ref_table_name = None
        self.__ref_col_name = None

    def consume(self, token_list: TokenList):
        match token_list.expect_type(TokenType.KEYWORD):
            case "check":
                # CHECK (logical_expression)
                token_list.consume_concrete("check")
                token_list.consume_concrete("(")
                t = token_list.consume_group(TLogicalExpression())
                token_list.consume_concrete(")")

                # To-do: Implement Check class
                # self.__constr_type = Check()
            case "constraint":
                # CONSTRAINT constraint_name
                token_list.consume_concrete("constraint")
                self.__constr_name = token_list.consume_of_type(TokenType.IDENTIFIER)
                self.consume(token_list)  # continuation in other cases
            case "default":
                # DEFAULT value
                token_list.consume_concrete("default")
                t = token_list.consume_group(TValue())

                # To-do: Implement Default class
                # self.__constr_type = Default()
            case "foreign":
                # FOREIGN KEY REFERENCES ref_table_name (ref_col_name)
                token_list.consume_concrete("foreign")
                token_list.consume_concrete("key")
                self.consume(token_list)  # continuation in "references" case
            case "not":
                token_list.consume_concrete("not")
                token_list.consume_concrete("null")

                # To-do: Implement NotNull class
                # self.__constr_type = NotNull()
            case "null":
                token_list.consume_concrete("null")

                # To-do: Implement Null class
                # self.__constr_type = Null()

            case "primary":
                token_list.consume_concrete("primary")
                token_list.consume_concrete("key")
                self.__constr_type = PrimaryKey([self.__src_col_name])
            case "references":
                # REFERENCES ref_table_name (ref_col_name)
                token_list.consume_concrete("references")
                self.__ref_table_name = token_list.consume_of_type(TokenType.IDENTIFIER)
                identifiers = token_list.consume_group(TIdentifiers())
                if len(identifiers.get_identifiers()) > 1:
                    raise SyntaxError("Multiple columns referenced in a single column constraint")
                self.__ref_col_name = identifiers.get_identifiers()[0]

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

                self.__constr_type = ForeignKey(
                    [self.__src_col_name],
                    self.__ref_table_name,
                    [self.__ref_col_name],
                    on_delete,
                    on_update,
                    self.__constr_name
                )
            case "unique":
                token_list.consume_concrete("unique")

                # To-do: Implement Unique class
                # self.__constr_type = Unique()
            case _:
                raise SyntaxError(f"Unexpected token at {token_list.peek()}")

    def get_constraint_name(self):
        return self.__constr_name

    def get_constraint_type(self):
        return self.__constr_type

    def get_source_column_name(self):
        return self.__src_col_name

    def get_referenced_table_name(self):
        return self.__ref_table_name

    def get_referenced_column_name(self):
        return self.__ref_col_name
