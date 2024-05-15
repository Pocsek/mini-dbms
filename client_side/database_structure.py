import json

from client_side.database_objects import Database
from client_side.server_connection import ServerConnection


class DatabaseStructure:
    """
    A class to store the skeleton of multiple databases with their tables and columns.
    The main use of this skeleton is to be able to access the names of the databases,
     tables and columns from the client side.
    """
    __databases: list[Database] = list()
    __working_db: int = 0  # the index of the database we're currently using

    def __init__(self, databases: list[Database] | None = None):
        if databases is None:
            self.__databases = list()
        else:
            self.__databases = databases

    def get_structure(self, connection: ServerConnection):
        """
        Get the structure of the databases from the server.
        :param connection: The connection to the server.
        """
        # TO-DO: Implement the get_structure method on the server side
        command: str = "get_structure"
        connection.send(command)
        response: str = connection.receive()
        self.from_dict(json.loads(response))

    def from_dict(self, data: dict) -> 'DatabaseStructure':
        self.__databases = [Database().from_dict(database) for database in data.get("databases", [])]
        self.__working_db = data.get("working_db", 0)
        return self

    def get_databases(self) -> list[Database]:
        return self.__databases

    def set_databases(self, databases: list[Database]):
        self.__databases = databases

    def add_database(self, database: Database):
        self.__databases.append(database)

    def remove_database(self, database: Database):
        self.__databases.remove(database)

    def get_database_names(self) -> list[str]:
        return [database.get_name() for database in self.__databases]

    def get_working_db_index(self) -> int:
        return self.__working_db
