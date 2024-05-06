"""NOT IMPLEMENTED"""

from server_side.interpreter.leaf_objects.constraint_node import ConstraintNode


class Default(ConstraintNode):
    def __init__(self, name=None):
        super().__init__(name)

    def check_validity(self):
        """
        Check if the column already has a constraint of this type.
        Check if the given default value matches the column's datatype.
        """
        pass
