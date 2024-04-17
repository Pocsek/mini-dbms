from client_side.database_objects.dbo import Dbo
from client_side.database_objects.table import Table


class Database(Dbo):
    __tables: list[Table] = list()

    def __init__(self, name: str = "", tables: list[Table] | None = None):
        self.__name = name
        if tables is None:
            self.__tables = list()
        else:
            self.__tables = tables

    def from_dict(self, data: dict):
        self.__name = data.get("name", "")
        self.__tables = [Table().from_dict(table) for table in data.get("tables", [])]
        return self

    def get_name(self) -> str:
        return self.__name

    def set_name(self, name: str):
        self.__name = name

    def get_tables(self) -> list[Table]:
        return self.__tables

    def set_tables(self, tables: list[Table]):
        self.__tables = tables

    def add_table(self, table: Table):
        self.__tables.append(table)

    def remove_table(self, table: Table):
        self.__tables.remove(table)

    def get_table_names(self) -> list[str]:
        return [table.get_name() for table in self.__tables]
