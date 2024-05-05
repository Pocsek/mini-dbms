"""NOT IMPLEMENTED"""
from dbmanager import DbManager
from .custom_tree import CustomTree


class ColumnConstraintDefinition(CustomTree):
    def __init__(self):
        super().__init__()

    def validate(self, dbm: DbManager = None, mongo_client=None):
        pass

    def connect_nodes_to_root(self) -> None:
        pass

    def connect_subtrees_to_root(self):
        pass

