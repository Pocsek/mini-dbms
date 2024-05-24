from server_side.interpreter.tree_objects.executable_tree import ExecutableTree
from server_side.database_objects import Index


class CreateIndex(ExecutableTree):
    def __init__(self):
        super().__init__()
        self.__index_name = ""
        self.__table_name = ""
        self.__column_names = []

    def _execute(self, dbm):
        table = dbm.get_table(dbm.get_working_db_index(), self.__table_name)
        index = Index(self.__index_name, self.__column_names)
        dbm.create_index(index, table.get_name())

    def validate(self, dbm, **kwargs):
        if not self.__index_name:
            raise AttributeError("IndexName not set")
        if not self.__table_name:
            raise AttributeError("TableName not set")
        if not self.__column_names:
            raise AttributeError("ColumnNames not set")
        # check if table exists
        db_idx = dbm.get_working_db_index()
        table_idx = dbm.find_table(db_idx, self.__table_name)
        if table_idx == -1:
            raise ValueError(f"Table [{self.__table_name}] does not exist in the database.")
        # check if columns exist
        existing_column_names = dbm.get_column_names(db_idx, table_idx)
        for column_name in self.__column_names:
            if column_name not in existing_column_names:
                raise ValueError(f"Column [{column_name}] does not exist in table [{self.__table_name}]")
        # check if index name is unique
        try:
            table = dbm.get_table(db_idx, self.__table_name)
            table.get_index(self.__index_name)
        except ValueError:
            raise ValueError(f"Index [{self.__index_name}] already exists in table [{self.__table_name}]")

    def connect_nodes_to_root(self):
        pass

    def connect_subtrees_to_root(self):
        pass

    def set_index_name(self, index_name: str):
        self.__index_name = index_name

    def set_table_name(self, table_name: str):
        self.__table_name = table_name

    def set_column_names(self, column_names: list[str]):
        self.__column_names = column_names

    def get_index_name(self) -> str:
        return self.__index_name

    def get_table_name(self) -> str:
        return self.__table_name

    def get_column_names(self) -> list[str]:
        return self.__column_names
