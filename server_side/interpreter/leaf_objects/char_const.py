from server_side.interpreter.leaf_objects.leaf_node import LeafNode


class CharConst(LeafNode):
    def __init__(self, value=""):
        super().__init__()
        self.__value = value

    def check_validity(self):
        pass

    def get_value(self):
        return self.__value
