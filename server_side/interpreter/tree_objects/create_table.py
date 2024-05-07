from server_side.dbmanager import DbManager
from server_side.interpreter.tree_objects.executable_tree import ExecutableTree
from server_side.interpreter.tree_objects.column_definitions import ColumnDefinitions
from server_side.interpreter.leaf_objects.char_const import CharConst
from server_side.interpreter.tree_objects.table_level_constraint_definitions import TableLevelConstraintDefinitions


class CreateTable(ExecutableTree):
    def __init__(self, name):
        super().__init__()
        self.__name = CharConst(name)
        self.__col_defs = ColumnDefinitions()
        self.__constr_defs = TableLevelConstraintDefinitions()

    def validate(self, dbm: DbManager = None, mongo_client=None):
        """
        Check if there already exists a table with the given name.
        """
        pass

    def _execute(self, dbm: DbManager = None, mongo_client=None):
        """
        Update the json structure with the new table.
        """
        pass

    def connect_nodes_to_root(self):
        self.add_node(self.__name, self.root)

    def connect_subtrees_to_root(self):
        self.paste(self.root, self.__col_defs)
        self.paste(self.root, self.__constr_defs)

    def get_name(self):
        return self.__name

    def get_column_definitions(self):
        return self.__col_defs

    def get_constraint_definitions(self):
        return self.__constr_defs

    def add_column_definition(self, col_def):
        self.__col_defs.paste(self.__col_defs.root, col_def)

    def add_constraint_definition(self, constr_def):
        self.__constr_defs.paste(self.__constr_defs_defs.root, constr_def)
