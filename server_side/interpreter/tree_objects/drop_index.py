from server_side.interpreter.tree_objects.executable_tree import ExecutableTree


class DropIndex(ExecutableTree):
    def __init__(self):
        super().__init__()

    def _execute(self, dbm):
        pass

    def validate(self, dbm, **kwargs):
        pass

    def connect_nodes_to_root(self):
        pass

    def connect_subtrees_to_root(self):
        pass

