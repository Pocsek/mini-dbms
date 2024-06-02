from server_side.interpreter.tree_objects.executable_tree import ExecutableTree


class DropIndex(ExecutableTree):
    def __init__(self):
        super().__init__()

    def _execute(self, dbm):
        pass

    def validate(self, dbm, **kwargs):
        pass
