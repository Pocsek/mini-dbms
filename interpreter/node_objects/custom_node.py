from abc import ABC, abstractmethod
from treelib import Node


class CustomNode(Node, ABC):
    def __init__(self, parent=None, tree_id=None):
        super().__init__(tag=self.__class__.__name__)
        self.set_initial_tree_id(tree_id)
        self.update_bpointer(parent)
        # self.set_predecessor()

    @abstractmethod
    def check_validity(self):
        pass
