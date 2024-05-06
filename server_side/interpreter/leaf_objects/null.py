"""NOT IMPLEMENTED"""

from server_side.interpreter.leaf_objects.constraint_node import ConstraintNode


class Null(ConstraintNode):
    def __init__(self, name=None):
        super().__init__(name)

    def check_validity(self):
        """
        Check if the column already has a constraint of this type.
        Check whether the column is a primary key.
        """
        pass


