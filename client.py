import json

from client_side.server_connection import ServerConnection
from client_side.database_structure import DatabaseStructure
from client_side.tab_completer import TabCompleter
from client_side.result import Result


CLI_COMMANDS = ["show databases", "show tables"]  # client-side commands
FORBIDDEN_COMMANDS = ["~show structure~"]  # commands that are not allowed to be sent by the client


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

        if command.lower() in CLI_COMMANDS + FORBIDDEN_COMMANDS:
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


def execute_cli_command(command: str, ds: DatabaseStructure):
    match command.lower():
        case "show databases":
            print("Databases: ", " ".join(ds.get_database_names()))
        case "show tables":
            print("Tables: ", " ".join(ds.get_table_names(ds.get_working_db_index())))


def interpret_response(response: str):
    decoded: dict = json.loads(response)
    message = decoded.get("message", None)
    results: list[dict] | None = decoded.get("results", None)
    if message:
        print(message)
    elif results:
        for r in results:
            result = Result().from_dict(r)
            if result.get_nr_rows_affected():
                print(f"{result.get_nr_rows_affected()} rows affected")
            # TODO: show result table


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
                if commands in CLI_COMMANDS:
                    execute_cli_command(commands, ds)
                    continue
                if commands in FORBIDDEN_COMMANDS:
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

# client should send the buffer size and the data after
