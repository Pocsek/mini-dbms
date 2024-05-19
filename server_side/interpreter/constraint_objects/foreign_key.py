from .cobj import CObj


class ForeignKey(CObj):
    def __init__(self, src_col_names, ref_table_name, ref_col_names, on_delete=None, on_update=None, constr_name=None):
        super().__init__(constr_name)
        self.__src_col_names = src_col_names
        self.__ref_table_name = ref_table_name
        self.__ref_col_names = ref_col_names
        self.__on_delete = on_delete if on_delete is not None else None
        self.__on_update = on_update if on_update is not None else None

    def validate(self, dbm, **kwargs):
        """
        Check if number of source columns is equal to the number of referenced columns.
        Check if the source column names are valid.
        Check whether the referenced table exists.
        Check whether the referenced columns exist.
        Check whether the referenced columns make a primary key or have unique constraint on them.

        "ON" clauses:
            - SET NULL is not allowed on source columns that are not nullable
            - SET DEFAULT is not allowed on source columns that are not nullable and do not have a default constraint
            - CASCADE ...
        """
        if len(self.__src_col_names) != len(self.__ref_col_names):
            raise ValueError(f"Number of source columns in FOREIGN KEY constraint is not equal to the number of "
                             f"referenced columns.")

        column_definitions = kwargs.get("column_definitions")
        if not column_definitions:
            raise ValueError(f"Column definitions not given in FOREIGN KEY constraint validation.")

        # column_definition = kwargs.get("column_definition")
        # if column_definition:  # the constraint is defined inside a column definition
        #     column_definition.validate_has_constraint_not_more_than_once(ForeignKey)
        # else:  # the constraint is a table constraint
        #
        #
        #
        # for col_name in self.__src_col_names:
        #     found = False
        #     for col_def in column_definitions:
        #         if col_def.get_name() == col_name:
        #             found = True


    def get_source_column_names(self):
        return self.__src_col_names

    def get_referenced_table_name(self):
        return self.__ref_table_name

    def get_referenced_column_names(self):
        return self.__ref_col_names

    def get_on_delete(self):
        return self.__on_delete

    def get_on_update(self):
        return self.__on_update
