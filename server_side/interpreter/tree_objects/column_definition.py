from server_side.interpreter.tree_objects.custom_tree import CustomTree
from server_side.interpreter.token_objects.tcolumn_definition import TColumnDefinition
from server_side.interpreter.constraint_objects import *


class ColumnDefinition(CustomTree):
    def __init__(self, tcol_def: TColumnDefinition):
        super().__init__()
        self.__name = tcol_def.get_name()
        self.__datatype = tcol_def.get_data_type()
        self.__col_constraints: list[CObj] = tcol_def.get_col_constraints()

    def validate(self, dbm, **kwargs):
        """
        Check if there is another column with the same name in the column definitions.
        Call the validate method of the column constraints.
        """
        col_defs: list[ColumnDefinition] | None = kwargs.get("column_definitions")
        if not col_defs:
            raise ValueError("List of column definitions not given in column definition validation.")

        for col_def in col_defs:
            if col_def == self:  # exclude self from the list
                continue
            if col_def.get_name() == self.__name:
                raise ValueError(f"Column with name '{self.__name}' already exists.")

        table_constraints: list[CObj] = kwargs.get("table_constraints")
        for col_constraint in self.__col_constraints:
            col_constraint.validate(dbm,
                                    column_definition=self,
                                    column_definitions=col_defs,
                                    table_constraints=table_constraints)

    def connect_nodes_to_root(self) -> None:
        pass

    def connect_subtrees_to_root(self):
        pass

    def get_name(self):
        return self.__name

    def get_datatype(self):
        return self.__datatype

    def get_col_constraints(self):
        return self.__col_constraints

    def is_allow_nulls(self):
        """
        A column cannot be null if:
            - it is part of a primary key
            - or has a "not null" constraint applied to it
        """
        for col_constraint in self.__col_constraints:
            if isinstance(col_constraint, PrimaryKey) or isinstance(col_constraint, NotNull):
                return False
            elif isinstance(col_constraint, Null):
                return True
        return True

    def get_identity_values(self):
        for col_constraint in self.__col_constraints:
            if isinstance(col_constraint, Identity):
                return col_constraint.get_seed(), col_constraint.get_increment()
        return None, None

    def get_default_value(self):
        for col_constraint in self.__col_constraints:
            if isinstance(col_constraint, Default):
                return col_constraint.get_default_value()
        return None

    def get_check(self):
        for col_constraint in self.__col_constraints:
            if isinstance(col_constraint, Check):
                return col_constraint
        return None

    def get_keys(self):
        keys = []
        for col_constraint in self.__col_constraints:
            if isinstance(col_constraint, PrimaryKey) \
                    or isinstance(col_constraint, ForeignKey) \
                    or isinstance(col_constraint, Unique):
                keys.append(col_constraint)
        return keys

    def has_constraint(self, constraint_type: type) -> bool:
        for col_constraint in self.__col_constraints:
            if isinstance(col_constraint, constraint_type):
                return True
        return False

    def validate_has_constraint_not_more_than_once(self, constraint_type: type):
        cnt = 0
        for col_constraint in self.__col_constraints:
            if isinstance(col_constraint, constraint_type):
                cnt += 1
                if cnt > 1:
                    raise ValueError(f"Column '{self.__name}': cannot have more than one '{constraint_type.__name__}' "
                                     f"constraints on the same column.")
