from .custom_node import CustomNode


class TableLevelConstraintDefinitions(CustomNode):
    def __init__(self, parent=None, tree_id=None):
        super().__init__(parent, tree_id)

    def check_validity(self):
        pass

    def add_constraint_definition(self, constr_def):
        constr_def.update_bpointer(self)
