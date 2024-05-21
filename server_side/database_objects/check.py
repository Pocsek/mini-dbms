from server_side.database_objects.dbo import Dbo


class Check(Dbo):
    """
    Check class.
    """
    def __init__(self, check_cobj=None):
        if check_cobj is not None:
            self.__constraint_name = check_cobj.get_constraint_name()
            self.__column_name = check_cobj.get_column_name()
            self.__op = check_cobj.get_op()
            self.__value = check_cobj.get_value()
        else:
            self.__constraint_name = ""
            self.__column_name = ""
            self.__op = ""
            self.__value = None

    def __dict__(self) -> dict:
        return {
            "constraint_name": self.__constraint_name,
            "column_name": self.__column_name,
            "op": self.__op,
            "value": self.__value
        }

    def from_dict(self, data: dict) -> 'Check':
        if not data:
            return self
        self.__constraint_name = data.get("constraint_name", "")
        self.__column_name = data.get("column_name", "")
        self.__op = data.get("op", "")
        self.__value = data.get("value", None)
        return self

    def get_name(self) -> str:
        return self.__constraint_name

    def get_column_name(self) -> str:
        return self.__column_name

    def get_op(self) -> str:
        return self.__op

    def get_value(self):
        return self.__value

    def set_name(self, name: str):
        self.__constraint_name = name
