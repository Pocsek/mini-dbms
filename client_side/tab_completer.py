import readline


class TabCompleter:
    """
    This class is used to provide tab completion for the user in the client.
    Completes database names and table names periodically.
    In the first iteration, it completes database names, after that, it completes table names, and so on.
    """
    __database_names = []
    __table_names = []
    # __column_names = []
    # __commands = ["use", "create", "drop", "alter", "insert", "select", "update", "delete", "exit"]

    def __init__(self):
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.complete_database)

    def set_database_names(self, database_names: list[str]):
        self.__database_names = database_names

    def set_table_names(self, table_names: list[str]):
        self.__table_names = table_names

    # def set_column_names(self, column_names: list[str]):
    #     self.__column_names = column_names

    # def set_commands(self, commands: list[str]):
    #     self.__commands = commands

    def complete_database(self, text, state):
        options = [db for db in self.__database_names if db.startswith(text)]
        if state < len(options):
            return options[state]
        else:
            readline.set_completer(self.complete_table)

    def complete_table(self, text, state):
        options = [tb for tb in self.__table_names if tb.startswith(text)]
        if state < len(options):
            return options[state]
        else:
            # readline.set_completer(self.complete_column)
            readline.set_completer(self.complete_database)

    # def complete_column(self, text, state):
    #     options = [col for col in self.__column_names if col.startswith(text)]
    #     if state < len(options):
    #         return options[state]
    #     else:
    #         # readline.set_completer(self.complete_command)
    #         readline.set_completer(self.complete_database)

    # def complete_command(self, text, state):
    #     options = [cmd for cmd in self.__commands if cmd.startswith(text)]
    #     if state < len(options):
    #         return options[state]
    #     else:
    #         readline.set_completer(self.complete_database)
