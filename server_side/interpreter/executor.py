from server_side.interpreter.tree_objects import ExecutableTree, Select


class Executor:
    """
    The Executor class is responsible for executing a list of ASTs (a.k.a. a list of commands).
    Keeps track of the execution status: whether the database was modified.
    """
    def __init__(self, dbm):
        self.__dbm = dbm  # DbManager instance
        self.__modified: bool = False
        # self.__nr_rows_affected = None
        self.__results: list = []  # list of Result objects

    def reset_state(self):
        self.__modified = False
        self.__results = []

    def modified(self):
        return self.__modified

    def execute(self, ast_list: list[ExecutableTree]):
        """
        Execute a list of ASTs (a.k.a. a list of commands).
        """
        self.reset_state()
        for ast in ast_list:
            if not isinstance(ast, Select):  # if the AST is not a SELECT statement
                self.__modified = True
            self.__execute_tree(ast)
            ast_result = ast.get_result()
            self.__results.append(ast_result)

    def __execute_tree(self, tree: ExecutableTree):
        """
        Execute a single AST.
        """
        tree.execute(self.__dbm)

    def get_results(self) -> list:
        return self.__results
