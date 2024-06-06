import json
import re
import tabulate

from client_side.server_connection import ServerConnection
from client_side.database_structure import DatabaseStructure
from client_side.tab_completer import TabCompleter
from client_side.result import Result
from client_side import __working_dir__  # the client_side directory's absolute path

# client side commands
CLI_COMMANDS = ["show databases", "show tables", r"file [\w/.:-]+", r"show columns [\w]+", "help"]
# commands that are not allowed to be sent by the client
FORBIDDEN_COMMANDS = ["~show structure~"]


def any_fullmatch(string: str, patterns: list[str]) -> bool:
    """
    Check if the string matches any of the patterns in the list.
    """
    for pattern in patterns:
        if re.fullmatch(pattern, string):
            return True
    return False


def get_user_input() -> (str, bool):
    nr: int = 0
    commands: str = ""
    while True:
        nr += 1
        command = input(f"{nr}> ").strip()
        match command.lower():
            case "go":
                return commands[:-1], True  # return commands string without trailing newline character
            case "exit":
                return "exit", False

        if any_fullmatch(command.lower(), CLI_COMMANDS + FORBIDDEN_COMMANDS):
            # if the command is a CLI or a FORBIDDEN command, return it immediately
            return command, True

        # the exit and go commands won't make it into the commands string
        if command != "":
            commands += command + "\n"


def get_database_structure(s: ServerConnection) -> DatabaseStructure:
    s.send("~show structure~")
    response = s.receive()
    structure: dict = json.loads(response)
    ds = DatabaseStructure()
    ds.from_dict(structure)
    return ds


def set_tab_completer(tab_completer: TabCompleter, ds: DatabaseStructure) -> TabCompleter:
    tab_completer.set_database_names(ds.get_database_names())
    tab_completer.set_table_names(ds.get_table_names(ds.get_working_db_index()))
    return tab_completer


def read_file(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def execute_cli_command(command: str, ds: DatabaseStructure, s: ServerConnection):
    """
    Execute a client side command.
    A client side command is a command that doesn't need to be sent to the server,
    but it's execution could include communication with the server.
    """
    match command.lower().split(" "):
        case ["show", "databases"]:
            db_names = ds.get_database_names()
            if db_names:
                print("Databases: ", " ".join(db_names))
            else:
                print("No databases found.")
        case ["show", "tables"]:
            tbl_names = ds.get_table_names(ds.get_working_db_index())
            if tbl_names:
                print("Tables: ", " ".join(tbl_names))
            else:
                db_name = ds.get_database_names()[ds.get_working_db_index()]
                print(f"No tables found in database '{db_name}'")
        case ["file", _]:
            # it important to use the filename from the original command and not the lowercase one
            path = command.split(" ")[1]
            try:
                commands = read_file(path)
            except FileNotFoundError:
                print(f"File '{path}' not found.")
                return
            if commands:
                print("Executing commands from file...")
                s.send(commands)
                interpret_response(s.receive())
            else:
                print("No commands to execute in file.")

        case ["show", "columns", _]:
            # it important to use the table name from the original command and not the lowercase one
            table_name = command.split(" ")[2]
            db_idx = ds.get_working_db_index()
            tb_idx = ds.find_table(db_idx, table_name)
            if tb_idx != -1:
                columns = ds.get_column_names(db_idx, tb_idx)
                if columns:
                    print("Columns: ", " ".join(columns))
                else:
                    print(f"No columns found in table '{table_name}'")

        case ["help"]:
            try:
                documentation = read_file(__working_dir__ + "/documentation.txt")
                print(documentation)
            except FileNotFoundError:
                print("No documentation found.")

        case _:
            print("Not implemented yet.")


def interpret_response(response: str):
    decoded: dict = json.loads(response)
    message = decoded.get("message", None)
    results: list[dict] | None = decoded.get("results", None)
    if message:
        print(message)
    elif results:
        for r in results:
            if r is None:
                print("No response from server on this command.")
                continue
            result = Result().from_dict(r)
            # print only one of the following field values of a response, because they should be mutually exclusive
            if result.get_response_message() is not None:
                print(result.get_response_message())
                continue
            if result.get_nr_rows_affected() is not None:
                print(f"{result.get_nr_rows_affected()} rows affected")
                continue
            if result.get_result_set() is not None:
                print(tabulate.tabulate(
                    tabular_data=result.get_result_set()[1],
                    headers=result.get_result_set()[0],
                    tablefmt="simple_grid"
                ))


def main():
    host = 'localhost'
    port = 12345
    try:
        s = ServerConnection(host, port)
    except ConnectionRefusedError:
        print("The server is not running.")
        return
    try:
        while True:
            ds = get_database_structure(s)
            tab_completer = set_tab_completer(TabCompleter(), ds)
            # print(ds.get_database_names(), ds.get_working_db_index())
            commands, keep_running = get_user_input()
            command_length: int = len(commands)
            if command_length != 0:
                if any_fullmatch(commands, CLI_COMMANDS):
                    execute_cli_command(commands, ds, s)
                    continue
                if any_fullmatch(commands, FORBIDDEN_COMMANDS):
                    print("This command is not allowed.")
                    continue
                s.send(commands)
                if keep_running:
                    interpret_response(s.receive())
                else:
                    s.close()
                    break
            else:
                print("No commands")
    except KeyboardInterrupt:
        print("Ctrl+C pressed")


main()
