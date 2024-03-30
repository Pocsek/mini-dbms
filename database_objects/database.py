from database_objects.dbo import Dbo
from database_objects.table import Table


class Database(Dbo):
    __tables: list[Table]

    def __init__(self, name: str):
        self.__name = name
        self.__tables = list()

    def __dict__(self) -> dict:
        return {
            "name": self.__name,
            "tables": [table.__dict__() for table in self.__tables]
        }

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