from database_objects.dbo import Dbo
from database_objects.column import Column


class Index(Dbo):
    __columns: list[Column] = list()
    __index: int = -1  # not sure if int will be the type

    def __init__(self,
                 name: str = "",
                 columns: list[Column] | None = None,
                 index: int = -1):
        if columns is None:
            columns = list()
        self.__name = name
        self.__columns = columns
        self.__index = index

    def __dict__(self) -> dict:
        return {
            "name": self.__name,
            "columns": [column.__dict__() for column in self.__columns],
            "index": self.__index
        }

    def from_dict(self, data: dict):
        self.__name = data.get("name", "")
        self.__columns = [Column().from_dict(column) for column in data.get("columns", [])]
        self.__index = data.get("index", -1)

    def get_name(self) -> str:
        return self.__name

    def get_columns(self) -> list[Column]:
        return self.__columns

    def get_index(self) -> int:
        return self.__index

    def set_name(self, name: str):
        self.__name = name

    def set_columns(self, columns: list[Column]):
        self.__columns = columns

    def set_index(self, index: int):
        self.__index = index
