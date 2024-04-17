from database_objects.dbo import Dbo


class PrimaryKey(Dbo):
    """
    Primary Key class.
    """
    __name: str = ""
    __column_names: list[str] = list()

    def __init__(self, name: str = "", column_names: list[str] | None = None):
        if column_names is None:
            column_names = list()
        self.__name = name
        self.__column_names = column_names

    def __dict__(self) -> dict:
        return {
            "name": self.__name,
            "column_names": self.__column_names
        }

    def from_dict(self, data: dict) -> 'PrimaryKey':
        if not data:
            return self
        self.__name = data.get("name", "")
        self.__column_names = data.get("column_names", [])
        return self

    def get_name(self) -> str:
        return self.__name

    def get_column_names(self) -> list[str]:
        return self.__column_names

    def set_name(self, name: str):
        self.__name = name

    def set_column_names(self, column_names: list[str]):
        self.__column_names = column_names




