from abc import ABC, abstractmethod
from custom_tree import CustomTree


class ExecutableTree(CustomTree, ABC):
    """
    A CustomTree on which execution can be called.
    """
    def __init__(self):
        super().__init__()

    @abstractmethod
    def execute(self):
        """Execute the tree."""
        pass
