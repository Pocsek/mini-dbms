from server_side.database_objects.dbo import Dbo
from server_side.database_objects.table import Table


class Database(Dbo):
    __tables: list[Table] = list()

    def __init__(self,
                 name: str = "",
                 tables: list[Table] | None = None):
        if tables is None:
            tables = list()
        self.__name = name
        self.__tables = tables

    def __dict__(self) -> dict:
        return {
            "name": self.__name,
            "tables": [table.__dict__() for table in self.__tables]
        }

    def from_dict(self, data: dict) -> 'Database':
        self.__name = data.get("name", "")
        self.__tables = [Table().from_dict(table) for table in data.get("tables", [])]
        return self

    def get_tables(self) -> list[Table]:
        return self.__tables

    def get_name(self) -> str:
        return self.__name

    def set_name(self, name: str):
        self.__name = name

    def add_table(self, table: Table):
        self.__tables.append(table)

    def get_table(self, name: str) -> Table | None:
        for table in self.__tables:
            if table.get_name() == name:
                return table
        return None

    def remove_table(self, name: str):
        for idx, table in enumerate(self.__tables):
            if table.get_name() == name:
                self.__tables.pop(idx)
                return
