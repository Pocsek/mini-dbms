from abc import ABC, abstractmethod
from treelib import Tree


class CustomTree(Tree, ABC):
    def __init__(self, parent=None):
        super().__init__()
        self.create_node(self.__class__.__name__)
        # self.update_bpointer(parent)
        # self.set_predecessor()

    @abstractmethod
    def check_validity(self):
        pass
