from server_side.interpreter.token_objects.tobj import TObj
from server_side.interpreter.token_classification import TokenType
from server_side.interpreter.token_list import TokenList


class TOptionalOnDeleteOrUpdate(TObj):
    """
    Consumes the following grammar:
        ON DELETE { NO ACTION | CASCADE | SET NULL | SET DEFAULT }
            or
        ON UPDATE { NO ACTION | CASCADE | SET NULL | SET DEFAULT }


    Optional in the class name means that if it does not find an "ON ..." clause, it simply leaves the instance empty
    without raising an exception.
    """

    def __init__(self):
        self.__type = None  # { DELETE | UPDATE }
        self.__action = None  # { NO ACTION | CASCADE | SET NULL | SET DEFAULT }

    def consume(self, token_list: TokenList):
        if token_list.peek() != "on":
            return
        token_list.consume_concrete("on")
        self.__type = token_list.consume_either(["delete", "update"])

        behavior_first = token_list.consume_either(["no", "cascade", "set"])
        match behavior_first:
            case "no":
                token_list.consume_concrete("action")
                self.__action = "no action"
            case "cascade":
                self.__action = "cascade"
            case "set":
                behavior_second = token_list.consume_either(["null", "default"])
                if behavior_second == "null":
                    self.__action = "set null"
                else:
                    self.__action = "set default"

    def get_type(self):
        return self.__type

    def get_action(self):
        return self.__action

    def exists(self):
        return self.__type is not None and self.__action is not None
