from chain_of_commands import ChainOfCommands


class Command:
    __name: str
    __terminal: bool
    __chain: ChainOfCommands

    def __init__(self, name: str, terminal: bool):
        self.__name = name
        self.__terminal = terminal

    def get_name(self) -> str:
        return self.__name

    def get_terminal(self) -> bool:
        return self.__terminal

    def set_name(self, name: str):
        self.__name = name

    def set_terminal(self, terminal: bool):
        self.__terminal = terminal

    def get_chain(self) -> ChainOfCommands:
        return self.__chain

    def set_chain(self, chain: ChainOfCommands):
        self.__chain = chain

    def check(self, tokens: list[str]) -> (list[str], bool, str) or (list[str], bool):
        # it should check if it can interpret the tokens
        # if yes and it is a terminal command then it should complete its function
        # if yes and it is not terminal it should pass down the tokens on its chain of commands
        # if no than it should signal it with a false state and send back the original tokens without a message
        # returns not used tokens, a state of execution, and if needed a message
        pass
