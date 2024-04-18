from abc import ABC, abstractmethod
from treelib import Node


class LeafNode(Node, ABC):
    def __init__(self):
        super().__init__(tag=self.__class__.__name__)

    @abstractmethod
    def check_validity(self):
        pass
