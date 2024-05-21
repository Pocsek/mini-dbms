from abc import ABC, abstractmethod
from treelib import Tree


class CustomTree(Tree, ABC):
    """
    A Tree that has a root node and some additional methods.
    """

    def __init__(self):
        super().__init__()
        self.create_node(self.__class__.__name__)  # add root node

    @abstractmethod
    def validate(self, dbm, **kwargs):
        """
        Check if any rules are being violated during execution. If so, then raise an exception.

        :param dbm: DbManager object
        """
        pass

    @abstractmethod
    def connect_nodes_to_root(self):
        """"""
        pass

    @abstractmethod
    def connect_subtrees_to_root(self):
        """
        A Tree cannot directly have a Tree child.
        Thus while building the tree we need to keep its subtrees disconnected from the root.
        And only when we are done with building the subtrees we connect them to the root.
        """
        pass

    def finalize(self):
        """
        Connect all nodes and subtrees to the root.
        MUST be called after the tree is built.
        """
        self.connect_nodes_to_root()
        self.connect_subtrees_to_root()
