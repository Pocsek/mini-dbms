from server_side.interpreter.tree_objects.executable_tree import ExecutableTree


class DropTable(ExecutableTree):
    def __init__(self):
        super().__init__()

    def _execute(self, dbm=None, mongo_client=None):
        pass

    def validate(self, dbm=None, mongo_client=None):
        pass

    def connect_nodes_to_root(self):
        pass

    def connect_subtrees_to_root(self):
        pass

