from abc import ABC, abstractmethod


class Dbo(ABC):
    __constraint_name: str = ""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __dict__(self) -> dict:
        pass

    @abstractmethod
    # load data from a dictionary into the object and return the object
    def from_dict(self, data: dict):
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def set_name(self, name: str):
        pass
