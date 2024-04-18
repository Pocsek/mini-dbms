from .custom_node import CustomNode


class InlineConstraintDefinitions(CustomNode):
    def __init__(self, parent=None):
        super().__init__(parent)

    def check_validity(self):
        pass

    def add_constraint_definition(self, constr_def):
        constr_def.update_bpointer(self)
