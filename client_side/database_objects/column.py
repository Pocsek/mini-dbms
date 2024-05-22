from client_side.database_objects.dbo import Dbo


class Column(Dbo):
    def __init__(self, name: str = ""):
        self.__name = name

    def from_dict(self, data: dict):
        self.__name = data.get("name", "")
        return self

    def get_name(self) -> str:
        return self.__name

    def set_name(self, name: str):
        self.__name = name
