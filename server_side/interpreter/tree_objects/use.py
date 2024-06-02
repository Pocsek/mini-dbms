from server_side.interpreter.tree_objects.executable_tree import ExecutableTree


class Use(ExecutableTree):
    def __init__(self, db_name):
        super().__init__()
        self.__db_name = db_name

    def validate(self, dbm, **kwargs):
        """
        Check if a database with the given name exists.
        """
        if dbm.find_database(self.__db_name) == -1:
            raise ValueError(f"Database '{self.__db_name}' does not exist.")

    def _execute(self, dbm):
        """
        Change the working DB.
        """
        dbm.set_working_db_index(dbm.find_database(self.__db_name))
        resp_message = f"Changed database context to '{self.__db_name}'."
        self.get_result().set_response_message(resp_message)
        print(resp_message)

    def get_name(self):
        return self.__db_name

