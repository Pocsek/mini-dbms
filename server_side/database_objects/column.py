from server_side.database_objects.dbo import Dbo


class Column(Dbo):
    def __init__(self,
                 name: str = "",
                 data_type: str = "",
                 allow_nulls: bool = True,
                 identity: bool = False,
                 identity_seed: int = 0,
                 identity_increment: int = 0,
                 default_value=None):
        self.__name = name
        self.__type = data_type
        self.__allow_nulls = allow_nulls
        self.__identity = identity
        self.__identity_seed = identity_seed
        self.__identity_increment = identity_increment
        self.__default_value = default_value

    def __dict__(self) -> dict:
        return {
            "name": self.__name,
            "type": self.__type,
            "allow_nulls": self.__allow_nulls,
            "identity": self.__identity,
            "identity_seed": self.__identity_seed,
            "identity_increment": self.__identity_increment,
            "default_value": self.__default_value
        }

    def from_dict(self, data: dict) -> 'Column':
        self.__name = data.get("name", "")
        self.__type = data.get("type", "")
        self.__allow_nulls = data.get("allow_nulls", True)
        self.__identity = data.get("identity", False)
        self.__identity_seed = data.get("identity_seed", 0)
        self.__identity_increment = data.get("identity_increment", 0)
        self.__default_value = data.get("default_value", None)
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

    def get_default_value(self):
        return self.__default_value

    def set_name(self, name: str):
        self.__name = name

    def set_type(self, _type: str):
        self.__type = _type

    def set_allow_nulls(self, allow_nulls: bool):
        self.__allow_nulls = allow_nulls

    def set_identity(self, identity_values: tuple[int, int] | tuple[None, None]):
        identity_seed, identity_increment = identity_values
        self.__identity = identity_seed is not None and identity_increment is not None
        self.__identity_seed = identity_seed
        self.__identity_increment = identity_increment

    def set_default_value(self, default_value):
        self.__default_value = default_value
