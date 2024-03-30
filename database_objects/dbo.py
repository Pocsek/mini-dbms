from abc import ABC, abstractmethod


class Dbo(ABC):
    __name: str

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __dict__(self) -> dict:
        pass
