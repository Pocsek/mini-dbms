from .custom_node import CustomNode


class ColumnDefinitions(CustomNode):
    def __init__(self, parent=None, tree_id=None):
        super().__init__(parent, tree_id)

    def check_validity(self):
        pass

    def add_column_definition(self, col_def):
        col_def.update_bpointer(self)
