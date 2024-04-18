from abc import ABC, abstractmethod
from treelib import Tree


class CustomTree(Tree, ABC):
    def __init__(self):
        super().__init__()
        self.create_node(self.__class__.__name__)  # add root node

    @abstractmethod
    def check_validity(self) -> None:
        """Check no rules are being violated ON EXECUTION."""
        pass

    @abstractmethod
    def connect_nodes_to_root(self) -> None:
        """"""
        pass

    @abstractmethod
    def connect_subtrees_to_root(self):
        """
        A Tree cannot directly have a Tree child.
        Thus while building the tree we need to keep its subtrees disconnected from the root.
        And only when we are done with building the subtrees we connect them to the root.

        # :return: A tree where all subtrees are connected to the root.
        """
        pass

    def finalize(self):
        """Connect all nodes and subtrees to the root."""
        self.connect_nodes_to_root()
        self.connect_subtrees_to_root()
