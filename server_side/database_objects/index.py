from server_side.database_objects.dbo import Dbo
from server_side.database_objects.column import Column


class Index(Dbo):
    def __init__(self,
                 name: str = "",
                 column_names: list[str] | None = None):
        if column_names is None:
            column_names = list()
        self.__name: str = name
        self.__column_names: list[str] = column_names

    def __dict__(self) -> dict:
        return {
            "name": self.__name,
            "column_names": self.__column_names
        }

    def from_dict(self, data: dict) -> 'Index':
        self.__name = data.get("name", "")
        self.__column_names = data.get("column_names", [])
        return self

    def get_name(self) -> str:
        return self.__name

    def get_column_names(self) -> list[str]:
        return self.__column_names

    def set_name(self, name: str):
        self.__name = name

    def set_columns(self, columns: list[Column]):
        self.__column_names = columns
