from abc import ABC, abstractmethod


class CustomTree(ABC):
    """
    A Tree that has a root node and some additional methods.
    """

    def __init__(self):
        super().__init__()

    @abstractmethod
    def validate(self, dbm, **kwargs):
        """
        Check if any rules are being violated during execution. If so, then raise an exception.

        :param dbm: DbManager object
        """
        pass
