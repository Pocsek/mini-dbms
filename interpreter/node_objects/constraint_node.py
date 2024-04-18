from abc import ABC, abstractmethod
from .custom_node import CustomNode
from .char_const import CharConst


class ConstraintNode(CustomNode, ABC):
    def __init__(self, name=None, parent=None):
        super().__init__(parent)
        self.__name = CharConst(self, name)

    def get_name(self):
        return self.__name

