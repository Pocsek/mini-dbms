from abc import ABC, abstractmethod
from .leaf_node import LeafNode


class ConstraintNode(LeafNode, ABC):
    def __init__(self, name=None):
        super().__init__()
        self.__name = name

    def get_name(self):
        return self.__name

