from .custom_node import CustomNode


class CharConst(CustomNode):
    def __init__(self, parent=None, tree_id=None, value=""):
        super().__init__(parent, tree_id)
        self.__value = value

    def check_validity(self):
        pass
