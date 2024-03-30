from command import Command


class ChainOfCommands:
    __ch: list[Command]
    __repeatable: bool = False

    def __init__(self, ch: list[Command], repeatable: bool = False):
        self.__ch = ch
        self.__repeatable = repeatable

    def __iter__(self):
        return self.__ch

    def repeatable(self) -> bool:
        return self.__repeatable

    def set_repeatable(self, repeatable: bool) -> None:
        self.__repeatable = repeatable

    def check_commands(self, tokens_param: list[str]) -> (list[str], bool, str):
        # it iterates through the commands in the chain
        # if one of them checks out
        # if its repeatable it restarts the chain for the remaining tokens
        # if not it terminates with an ok status
        # returns not used tokens, a state of execution, and the message returned from the command
        tokens = tokens_param
        i: int = 0
        while i < len(self.__ch):
            tks, ok, msg = self.__ch[i].check(tokens)
            if ok:
                if self.__repeatable:
                    i = 0  # restart the chain
                    tokens = tks  # update tokens
                else:
                    return tks, ok, msg
            else:
                i += 1

