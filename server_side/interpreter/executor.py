from server_side.dbmanager import DbManager

from server_side.interpreter.tree_objects import ExecutableTree


class Executor:
    """
    The Executor class is responsible for executing a list of ASTs (a.k.a. a list of commands).
    Keeps track of the execution status: whether the database was modified.
    """
    def __init__(self, dbm: DbManager):
        self.__dbm = dbm
        self.__modified = None
        self.__nr_rows_affected = None

    def reset_state(self):
        self.__modified = False
        self.__nr_rows_affected = 0

    def modified(self):
        return self.__modified

    def execute(self, ast_list: list[ExecutableTree]):
        """
        Execute a list of ASTs (a.k.a. a list of commands).
        """
        for ast in ast_list:
            self.__execute_tree(ast)

    def __execute_tree(self, tree: ExecutableTree):
        """
        Execute a single AST.
        """
        self.reset_state()
        tree.execute(self.__dbm)
