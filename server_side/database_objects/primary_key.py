from server_side.database_objects.dbo import Dbo


class PrimaryKey(Dbo):
    """
    Primary Key class.
    """
    def __init__(self, primary_key_cobj=None, constraint_name: str = "", column_names: list[str] | None = None):
        if primary_key_cobj is not None:
            self.__constraint_name = primary_key_cobj.get_constraint_name()
            self.__column_names = primary_key_cobj.get_column_names()
        else:
            if column_names is None:
                column_names = list()
            self.__constraint_name = constraint_name
            self.__column_names = column_names

    def __dict__(self) -> dict:
        return {
            "constraint_name": self.__constraint_name,
            "column_names": self.__column_names
        }

    def from_dict(self, data: dict) -> 'PrimaryKey':
        if not data:
            return self
        self.__constraint_name = data.get("constraint_name", "")
        self.__column_names = data.get("column_names", [])
        return self

    def get_name(self) -> str:
        return self.__constraint_name

    def get_column_names(self) -> list[str]:
        return self.__column_names

    def set_name(self, name: str):
        self.__constraint_name = name

    def set_column_names(self, column_names: list[str]):
        self.__column_names = column_names




