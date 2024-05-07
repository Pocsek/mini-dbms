from abc import ABC
from server_side.interpreter.leaf_objects.leaf_node import LeafNode


class ConstraintNode(LeafNode, ABC):
    def __init__(self, name=None):
        super().__init__()
        self.__name = name

    def get_name(self):
        return self.__name

