from client_side.database_objects.column import Column
from client_side.database_objects.dbo import Dbo


class Table(Dbo):
    __columns: list[Column] = list()

    def __init__(self, name: str = "", columns: list[Column] | None = None):
        self.__name = name
        if columns is None:
            self.__columns = list()
        else:
            self.__columns = columns

    def from_dict(self, data: dict):
        self.__name = data.get("name", "")
        self.__columns = [Column("").from_dict(column) for column in data.get("columns", [])]
        return self

    def get_name(self) -> str:
        return self.__name

    def set_name(self, name: str):
        self.__name = name

    def get_columns(self) -> list[Column]:
        return self.__columns

    def set_columns(self, columns: list[Column]):
        self.__columns = columns

    def add_column(self, column: Column):
        self.__columns.append(column)

    def remove_column(self, column: Column):
        self.__columns.remove(column)

    def get_column_names(self) -> list[str]:
        return [column.get_name() for column in self.__columns]
