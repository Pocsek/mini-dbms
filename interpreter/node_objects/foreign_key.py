from .constraint_node import ConstraintNode


class ForeignKey(ConstraintNode):
    def __init__(self, name=None, parent=None):
        super().__init__(name, parent)

    def check_validity(self):
        """
        Check if the column already has a constraint of this type.
        Check whether the referenced table exists.
        Check whether the referenced column exists.
        Check whether the referenced column is a primary key or has a unique constraint on it.
        """
        pass


