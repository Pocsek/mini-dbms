from server_side.database_objects.dbo import Dbo


class ForeignKey(Dbo):
    """
    Foreign Key class.
    """
    def __init__(self, foreign_key_cobj=None):
        if foreign_key_cobj is not None:
            self.__constraint_name = foreign_key_cobj.get_constraint_name()
            self.__src_col_names = foreign_key_cobj.get_source_column_names()
            self.__ref_table_name = foreign_key_cobj.get_referenced_table_name()
            self.__ref_col_names = foreign_key_cobj.get_referenced_column_names()
            self.__on_delete = foreign_key_cobj.get_on_delete()
            self.__on_update = foreign_key_cobj.get_on_update()
        else:
            self.__constraint_name = ""
            self.__src_col_names = []
            self.__ref_table_name = ""
            self.__ref_col_names = []
            self.__on_delete = None
            self.__on_update = None

    def __dict__(self) -> dict:
        return {
            "constraint_name": self.__constraint_name,
            "source_column_names": self.__src_col_names,
            "referenced_table_name": self.__ref_table_name,
            "referenced_column_names": self.__ref_col_names,
            "on_delete": self.__on_delete,
            "on_update": self.__on_update
        }

    def from_dict(self, data: dict) -> 'ForeignKey':
        if not data:
            return self
        self.__constraint_name = data.get("constraint_name", "")
        self.__src_col_names = data.get("source_column_names", [])
        self.__ref_table_name = data.get("referenced_table_name", "")
        self.__ref_col_names = data.get("referenced_column_names", [])
        self.__on_delete = data.get("on_delete", None)
        self.__on_update = data.get("on_update", None)
        return self

    def get_name(self) -> str:
        return self.__constraint_name

    def set_name(self, name: str):
        self.__constraint_name = name

