from server_side.interpreter.tree_objects.executable_tree import ExecutableTree
from server_side.interpreter.leaf_objects.char_const import CharConst


class CreateDatabase(ExecutableTree):
    def __init__(self, db_name):
        super().__init__()
        self.__db_name = CharConst(db_name)

    def validate(self, dbm, **kwargs):
        """
        Check if there already exists a database with the given name.
        """
        if dbm.find_database(self.__db_name.get_value()) != -1:
            raise ValueError(f"Database with name '{self.__db_name.get_value()}' already exists.")

    def _execute(self, dbm):
        """
        Update the json structure with the new database.
        """
        from server_side.database_objects import Database
        new_db = Database(self.__db_name.get_value())
        dbm.add_database(new_db)
        dbm.update_db_structure_file()
        print(f"Database '{self.__db_name.get_value()}' created successfully.")

    def connect_nodes_to_root(self):
        self.add_node(self.__db_name, self.root)

    def connect_subtrees_to_root(self):
        pass

    def get_name(self):
        return self.__db_name

