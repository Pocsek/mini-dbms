"""NOT IMPLEMENTED"""

from .constraint_node import ConstraintNode


class Identity(ConstraintNode):
    def __init__(self, name=None):
        super().__init__(name)

    def check_validity(self):
        """
        Check if the column already has a constraint of this type.
        Check if the seed and increment values are valid.
        """
        pass
