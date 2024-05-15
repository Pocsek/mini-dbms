from abc import ABC, abstractmethod


class Dbo(ABC):
    __name: str = ""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    # load data from a dictionary
    def from_dict(self, data: dict):
        """Set the object's attributes from a dictionary. Return the object."""
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def set_name(self, name: str):
        pass
