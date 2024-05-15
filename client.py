import json

from client_side.server_connection import ServerConnection
from client_side.database_structure import DatabaseStructure


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
            case "~show structure~":
                # not a command the client can use
                return "", True
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
            print(ds.get_database_names(), ds.get_working_db_index())
            commands, keep_running = get_user_input()
            command_length: int = len(commands)
            if command_length != 0:
                s.send(commands)
                if keep_running:
                    response = s.receive()
                    print(response)
                else:
                    s.close()
                    break
            else:
                print("No commands")
    except KeyboardInterrupt:
        print("Ctrl+C pressed")


main()

# client should send the buffer size and the data after
