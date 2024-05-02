from abc import ABC, abstractmethod
from .custom_tree import CustomTree
from dbmanager import DbManager


class ExecutableTree(CustomTree, ABC):
    """
    A type of CustomTree where an execution chain can be started from the root.
    """
    def __init__(self):
        super().__init__()

    @abstractmethod
    def _execute(self, dbm: DbManager = None, mongo_client=None):
        pass

    def execute(self, dbm: DbManager = None, mongo_client=None):
        """
        Perform validation, then execute the tree.
        """

        # method of CustomTree which calls the validate method on all of its children
        self.validate(dbm, mongo_client)

        # method of ExecutableTree which calls the execute method of all its ExecutableTree children
        self._execute(dbm, mongo_client)

