class Result:
    """
    Has tree mutually exclusive fields:

    nr_rows_affected: int | None
    result_set: tuple[list[str], list[list]] | None
    response_message: str | None

    After each command execution, the server should send a response containing the result of the command.
    This result will set only one field of the Result object, depending on the type of the command:

    - Delete:  number of rows deleted
    - Insert: number of rows inserted
    - Select: rows selected - a tuple containing the column names and the rows
    - Create: message if creation was successful
    - Drop: message if drop was successful
    """

    def __init__(self):
        self.__nr_rows_affected: int | None = None
        self.__result_set: tuple[list[str], list[list]] | None = None  # (<col_names>, <rows>)
        self.__response_message: str | None = None

    def from_dict(self, result_dict: dict) -> 'Result':
        self.set_nr_rows_affected(result_dict.get("nr_rows_affected"))
        self.set_result_set(result_dict.get("result_set"))
        self.set_response_message(result_dict.get("response_message"))
        return self

    def set_nr_rows_affected(self, nr_rows_affected: int):
        self.__nr_rows_affected = nr_rows_affected

    def set_result_set(self, result_set: tuple[list[str], list[list]]):
        self.__result_set = result_set

    def get_nr_rows_affected(self) -> int | None:
        return self.__nr_rows_affected

    def get_result_set(self) -> tuple[list[str], list[list]] | None:
        return self.__result_set

    def set_response_message(self, response_message: str):
        self.__response_message = response_message

    def get_response_message(self) -> str | None:
        return self.__response_message


