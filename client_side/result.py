class Result:
    """
    - Delete:  number of rows deleted
    - Insert: Ids of inserted rows or number of rows inserted
    - Select: rows selected
    - Create: if creation was successful, or error message
    - Drop: if drop was successful, or error message
    maybe store the ASTs that were executed so we know what was done
    """

    def __init__(self):
        self.__nr_rows_affected: int | None = None
        self.__result_set: tuple[list[str], list[list]] | None = None  # (<col_names>, <rows>)

    def from_dict(self, result_dict: dict):
        self.set_nr_rows_affected(result_dict.get("nr_rows_affected"))
        self.set_result_set(result_dict.get("result_set"))

    def set_nr_rows_affected(self, nr_rows_affected: int):
        self.__nr_rows_affected = nr_rows_affected

    def set_result_set(self, result_set: tuple[list[str], list[list]]):
        self.__result_set = result_set

    def get_nr_rows_affected(self) -> int | None:
        return self.__nr_rows_affected

    def get_result_set(self) -> tuple[list[str], list[list]] | None:
        return self.__result_set


