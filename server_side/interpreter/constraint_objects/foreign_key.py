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
        Check whether the source columns exist.
        Check if the source columns already have a constraint of this type.
        Check whether the referenced table exists.
        Check whether the referenced columns exist.
        Check whether the referenced columns make a primary key or have unique constraint on them.
        :param **kwargs:
        """
        pass

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
