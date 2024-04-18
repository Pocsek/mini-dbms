from .constraint_node import ConstraintNode


class Null(ConstraintNode):
    def __init__(self, name=None, parent=None):
        super().__init__(name, parent)

    def check_validity(self):
        """
        Check if the column already has a constraint of this type.
        Check whether the column is a primary key.
        """
        pass


