from server_side.database_objects.column import Column
from server_side.database_objects.dbo import Dbo
from server_side.database_objects.index import Index
from server_side.database_objects.primary_key import PrimaryKey


class Table(Dbo):
    __columns: list[Column] = list()
    __indexes: list[Index] = list()
    __primary_key: PrimaryKey | None = None

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
            "indexes": [index.__dict__() for index in self.__indexes],
            "primary_key": self.__primary_key.__dict__() if self.__primary_key is not None else {}
        }

    def from_dict(self, data: dict) -> 'Table':
        self.__name = data.get("name", "")
        self.__columns = [Column().from_dict(column) for column in data.get("columns", [])]
        self.__indexes = [Index().from_dict(index) for index in data.get("indexes", [])]
        pk_dict = data.get("primary_key", {})
        if pk_dict:  # ensure that the primary key was provided
            self.__primary_key = PrimaryKey().from_dict(pk_dict)
        else:
            self.__primary_key = None
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

    def get_primary_key(self) -> PrimaryKey:
        return self.__primary_key

    def set_primary_key(self, primary_key: PrimaryKey):
        self.__primary_key = primary_key

    def get_column_names(self) -> list[str]:
        return [col.get_name() for col in self.__columns]

    def has_primary_key(self) -> bool:
        return self.__primary_key is not None
