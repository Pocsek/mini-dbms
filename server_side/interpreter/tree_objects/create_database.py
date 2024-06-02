from server_side.interpreter.tree_objects.executable_tree import ExecutableTree


class CreateDatabase(ExecutableTree):
    def __init__(self, db_name):
        super().__init__()
        self.__db_name = db_name

    def validate(self, dbm, **kwargs):
        """
        Check if there already exists a database with the given name.
        """
        if dbm.find_database(self.__db_name) != -1:
            raise ValueError(f"Database with name '{self.__db_name}' already exists.")

    def _execute(self, dbm):
        """
        Update the json structure with the new database.
        """
        from server_side.database_objects import Database
        new_db = Database(self.__db_name)
        dbm.add_database(new_db)
        dbm.update_db_structure_file()
        resp_message = f"Database '{new_db.get_name()}' created successfully."
        self.get_result().set_response_message(resp_message)
        print(resp_message)

    def get_name(self):
        return self.__db_name

