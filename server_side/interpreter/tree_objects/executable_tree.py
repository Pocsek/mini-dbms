from abc import ABC, abstractmethod
from server_side.interpreter.tree_objects.custom_tree import CustomTree


class ExecutableTree(CustomTree, ABC):
    """
    A type of CustomTree where an execution chain can be started from the root.
    """
    def __init__(self):
        super().__init__()

    @abstractmethod
    def _execute(self, dbm=None, mongo_client=None):
        pass

    def execute(self, dbm=None, mongo_client=None):
        """
        Perform validation, then execute the tree.

        :param dbm: DbManager object
        :param mongo_client: MongoClient object
        """

        # method of CustomTree which calls the validate method on all of its children
        self.validate(dbm, mongo_client)

        # method of ExecutableTree which calls the execute method of all its ExecutableTree children
        self._execute(dbm, mongo_client)

