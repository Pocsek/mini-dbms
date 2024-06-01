from abc import ABC, abstractmethod
from server_side.interpreter.tree_objects.custom_tree import CustomTree


class ExecutableTree(CustomTree, ABC):
    """
    A type of CustomTree where an execution chain can be started from the root.
    """
    def __init__(self):

        self.__result = None  # the result of the execution, an instance of the Result class
        super().__init__()

    @abstractmethod
    def _execute(self, dbm):
        pass

    def execute(self, dbm):
        """
        Perform validation, then execute the tree.

        :param dbm: DbManager object
        """

        # method of CustomTree which calls the validate method on all of its children
        self.validate(dbm)

        # method of ExecutableTree which calls the execute method of all its ExecutableTree children
        self._execute(dbm)

