from database_objects.dbo import Dbo


class Column(Dbo):
    __type: str = ""
    __allow_nulls: bool = True
    __identity: bool = False
    __identity_seed: int = 0
    __identity_increment: int = 0

    def __init__(self,
                 name: str = "",
                 data_type: str = "",
                 allow_nulls: bool = True,
                 identity: bool = False,
                 identity_seed: int = 0,
                 identity_increment: int = 0):
        self.__name = name
        self.__type = data_type
        self.__allow_nulls = allow_nulls
        self.__identity = identity
        self.__identity_seed = identity_seed
        self.__identity_increment = identity_increment

    def __dict__(self) -> dict:
        return {
            "name": self.__name,
            "type": self.__type,
            "allow_nulls": self.__allow_nulls,
            "identity": self.__identity,
            "identity_seed": self.__identity_seed,
            "identity_increment": self.__identity_increment
        }

    def from_dict(self, data: dict) -> 'Column':
        self.__name = data.get("name", "")
        self.__type = data.get("type", "")
        self.__allow_nulls = data.get("allow_nulls", True)
        self.__identity = data.get("identity", False)
        self.__identity_seed = data.get("identity_seed", 0)
        self.__identity_increment = data.get("identity_increment", 0)
        return self

    def get_name(self) -> str:
        return self.__name

    def get_type(self) -> str:
        return self.__type

    def get_allow_nulls(self) -> bool:
        return self.__allow_nulls

    def get_identity(self) -> bool:
        return self.__identity

    def get_identity_seed(self) -> int:
        return self.__identity_seed

    def get_identity_increment(self) -> int:
        return self.__identity_increment

    def set_name(self, name: str):
        self.__name = name

    def set_type(self, _type: str):
        self.__type = _type

    def set_allow_nulls(self, allow_nulls: bool):
        self.__allow_nulls = allow_nulls

    def set_identity(self, identity: bool):
        self.__identity = identity

    def set_identity_seed(self, identity_seed: int):
        self.__identity_seed = identity_seed

    def set_identity_increment(self, identity_increment: int):
        self.__identity_increment = identity_increment
