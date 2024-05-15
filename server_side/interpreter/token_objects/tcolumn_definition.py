from server_side.interpreter.constraint_objects import CObj
from server_side.interpreter.token_objects.tcolumn_constraint_definition import TColumnConstraintDefinition
from server_side.interpreter.token_objects.tobj import TObj

from server_side.interpreter.token_classification import TokenType
from server_side.interpreter.tree_objects.constraint_definition import ConstraintDefinition


class TColumnDefinition(TObj):
    """<column_name> <data_type> [ <column_constraint> [,... n] ]"""
    def __init__(self):
        self.__col_name = None
        self.__data_type = None
        self.__col_constraints: list[ConstraintDefinition] = []

    def consume(self, tokens):
        self.__col_name = tokens.consume_of_type(TokenType.IDENTIFIER)
        self.__data_type = tokens.consume_of_type(TokenType.DATATYPE)

        try:
            while tokens.peek() not in (",", ")"):
                col_constr_def = tokens.consume_group(TColumnConstraintDefinition())
                self.__col_constraints.append(ConstraintDefinition(col_constr_def))
        except IndexError:
            raise SyntaxError("Unexpected end of command. Expected ',' or ')'")

    def get_name(self):
        return self.__col_name

    def get_data_type(self):
        return self.__data_type

    def get_col_constraints(self):
        return self.__col_constraints
