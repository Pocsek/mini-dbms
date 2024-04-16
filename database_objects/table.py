from database_objects.column import Column
from database_objects.dbo import Dbo
from database_objects.index import Index


class Table(Dbo):
    __columns: list[Column] = list()
    __indexes: list[Index] = list()

    # TO-DO: add keys, create a key class, possibly one for each type of key
    # "keys": {
    #     "primary_key": [],
    #     "foreign_keys": [],
    #     "unique_keys": []
    # }

    def __init__(self,
                 name: str = "",
                 columns: list[Column] | None = None,
                 indexes: list[Index] | None = None):
        if columns is None:
            columns = list()
        if indexes is None:
            indexes = list()
        self.__name = name
        self.__columns = columns
        self.__indexes = indexes

    def __dict__(self) -> dict:
        return {
            "name": self.__name,
            "columns": [column.__dict__() for column in self.__columns],
            "indexes": [index.__dict__() for index in self.__indexes]
        }

    def from_dict(self, data: dict) -> 'Table':
        self.__name = data.get("name", "")
        self.__columns = [Column().from_dict(column) for column in data.get("columns", [])]
        self.__indexes = [Index().from_dict(index) for index in data.get("indexes", [])]
        return self

    def get_name(self) -> str:
        return self.__name

    def get_columns(self) -> list[Column]:
        return self.__columns

    def get_indexes(self) -> list[Index]:
        return self.__indexes

    def set_name(self, name: str):
        self.__name = name

    def set_columns(self, columns: list[Column]):
        self.__columns = columns

    def set_indexes(self, indexes: list[Index]):
        self.__indexes = indexes

    def add_column(self, column: Column):
        # TO-DO: check if the column already exists
        self.__columns.append(column)

    def add_index(self, index: Index):
        # TO-DO: check if the index already exists
        self.__indexes.append(index)
