from .cobj import CObj


class PrimaryKey(CObj):
    def __init__(self, column_names: list[str], constr_name=None):
        super().__init__(constr_name)
        self.__column_names = column_names

    def validate(self, dbm, **kwargs):
        """
        Rules:
            - Referenced columns should be existing columns.
            - A table can contain only one primary key constraint.
            - All columns defined within a primary key constraint must be defined as not null. If nullability isn't
            specified, all columns participating in a primary key constraint have their nullability set to not null.
        """
        column_definitions = kwargs.get("column_definitions")
        if not column_definitions:
            raise ValueError(f"Column definitions not given in PRIMARY KEY constraint validation.")

        table_constraints = kwargs.get("table_constraints", [])

        column_definition = kwargs.get("column_definition")
        if column_definition:  # the constraint is defined inside a column definition
            column_definition.validate_has_constraint_not_more_than_once(PrimaryKey)

            for col_def in column_definitions:
                if col_def == column_definition:  # exclude self from the list
                    continue
                if col_def.has_constraint(PrimaryKey):
                    raise ValueError(f"Column '{column_definition.get_name()}': cannot have more than one PRIMARY KEY "
                                     f"constraints on the same table.")

            for constr in table_constraints:
                if isinstance(constr, PrimaryKey):
                    raise ValueError(f"Column '{column_definition.get_name()}': cannot have more than one PRIMARY KEY "
                                     f"constraints on the same table.")
        else:  # the constraint is a table constraint
            for constr in table_constraints:
                if constr == self:  # exclude self from the list
                    continue
                if isinstance(constr, PrimaryKey):
                    raise ValueError(f"Table '{kwargs.get('table_name')}': cannot have more than one PRIMARY KEY "
                                     f"constraints on the same table.")

            from .null import Null
            for col_name in self.__column_names:
                found = False
                for col_def in column_definitions:
                    if col_def.get_name() == col_name:
                        if col_def.has_constraint(Null):
                            raise ValueError(f"Column '{col_name}': cannot be part of a PRIMARY KEY constraint "
                                             f"if it has a NULL constraint.")
                        found = True
                        break
                if not found:
                    raise ValueError(f"Invalid PRIMARY KEY column reference: '{col_name}'.")

    def get_column_names(self):
        return self.__column_names
