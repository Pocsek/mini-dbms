from dbmanager import DbManager
from interpreter.tree_objects.custom_tree import CustomTree
from interpreter.tree_objects.executable_tree import ExecutableTree
from interpreter.leaf_objects.char_const import CharConst
from interpreter.tree_objects.table_constraint_definition import TableConstraintDefinition
from database_objects import Table, Column


class CreateTable(ExecutableTree):
    def __init__(self):
        """
        In a CREATE TABLE statement, a constraint can be defined at the column level or at the table level.

        At the column level, a constraint is defined as part of a column definition, and is applied only to that column.
        At the table level, a constraint is defined as a table constraint, and can be applied to more than one column.
        """
        super().__init__()
        self.__name = ""
        self.__col_defs = []
        self.__table_constr_defs = []

    def validate(self, dbm: DbManager = None, mongo_client=None):
        """
        Check if there already exists a table with the given name.
        """
        pass

    def _execute(self, dbm: DbManager = None, mongo_client=None):
        """
        Update the json structure with the new table.
        """

        columns = Column()
        for col_def in self.__col_defs:
            pass




    def connect_nodes_to_root(self):
        pass

    def connect_subtrees_to_root(self):
        pass

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_column_definitions(self):
        return self.__col_defs

    def get_constraint_definitions(self):
        return self.__table_constr_defs

    def add_column_definition(self, col_def):
        self.__col_defs.append(col_def)

    def add_table_constraint_definition(self, constr_def):
        self.__table_constr_defs.append(constr_def)
