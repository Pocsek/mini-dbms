from .tobj import TObj
from ..token_list import TokenList
from ..token_classification import TokenType
from .tlogical_expression import TLogicalExpression
from .tvalue import TValue
from ..constraint_objects import *


class TColumnConstraintDefinition(TObj):
    """[CONSTRAINT constraint_name] constraint_type ( constraint_args )"""
    def __init__(self):
        self.__constr_name = None
        self.__constr_type = CObj()
        self.__src_col_name = None
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
                self.consume(token_list)
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
                token_list.consume_concrete("references")
                self.__ref_table_name = token_list.consume_of_type(TokenType.IDENTIFIER)
                token_list.consume_concrete("(")
                self.__ref_col_name = token_list.consume_of_type(TokenType.IDENTIFIER)
                token_list.consume_concrete(")")

                if token_list.peek() == "on":
                    token_list.consume_concrete("on")
                    operation_type = token_list.consume_either(["delete", "update"])  # DELETE or UPDATE

                    # temporary solution:
                    behavior_first = token_list.consume_either(["no", "cascade", "set"])
                    match behavior_first:
                        case "no":
                            token_list.consume_concrete("action")
                            # To-do
                        case "cascade":
                            # To-do
                            pass
                        case "set":
                            behavior_second = token_list.consume_either(["null", "default"])
                            if behavior_second == "null":
                                # To-do
                                pass
                            else:
                                # To-do
                                pass
                    # To-do:
                    # - add keywords NO ACTION, CASCADE, SET NULL, SET DEFAULT to token_classification.py

                # To-do: Implement ForeignKey class
                # self.__constr_type = ForeignKey()
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

                # To-do: Implement PrimaryKey class
                # self.__constr_type = PrimaryKey()
            case "references":
                # REFERENCES ref_table_name (ref_col_name)
                token_list.consume_concrete("references")
                self.__ref_table_name = token_list.consume_of_type(TokenType.IDENTIFIER)
                token_list.consume_concrete("(")
                self.__ref_col_name = token_list.consume_of_type(TokenType.IDENTIFIER)
                token_list.consume_concrete(")")

                # To-do: Implement ForeignKey class
                # self.__constr_type = ForeignKey()
            case "unique":
                token_list.consume_concrete("unique")

                # To-do: Implement Unique class
                # self.__constr_type = Unique()
            case _:
                raise SyntaxError(f"Unexpected token at {token_list.peek()}")
