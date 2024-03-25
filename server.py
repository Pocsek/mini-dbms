from socket import *
from threading import Thread
from datetime import datetime
import sys
import re

import dbmanager

stop_threads = False


def log(message: str, filename: str):
    f = open(filename, 'a')
    time = datetime.now()
    f.write(str(time) + " -- " + message + '\n')
    f.close()


def create_socket(host, port) -> socket:
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((host, port))
    sock.listen()
    return sock


def respond_to_client(client_socket: socket, commands: [str]):
    good: bool = True
    modified: bool = False
    response: str = ""
    n_cmd = len(commands)
    # do something with the commands
    for command in commands:
        # the true-false logic is not correct, but it will change anyway
        match command.lower().strip().split():
            case ["use", obj]:
                db_idx = dbmanager.find_database(obj)
                if db_idx == -1:
                    response = f"Database '{obj}' does not exist. Make sure that the name is entered correctly."
                    good = False
                else:
                    response = f"Changed database context to '{obj}'."
                    dbmanager.working_db = db_idx

            case ["create", *obj]:
                match obj:
                    # example command: create database test1
                    case ["database", db_name]:
                        db_idx = dbmanager.find_database(db_name)
                        if db_idx != -1:
                            response = f"Database '{db_name}' already exists. Choose a different database name."
                            good = False
                        else:
                            dbmanager.working_db = len(dbmanager.get_databases())
                            dbmanager.dbs["databases"].append({
                                "name": db_name,
                                "tables": []
                            })
                            modified = True

                    # example command: create table t1 ( ... );
                    case ["table", table_name, "(", *column_commands, ");"]:
                        new_table = dbmanager.create_empty_table()
                        new_table["name"] = table_name

                        column_definitions = []
                        tmp = []
                        for word in column_commands:
                            if word[-1] == ',':
                                tmp.append(word[:-1])
                                column_definitions.append(tmp)
                                tmp = []
                            else:
                                tmp.append(word)
                        column_definitions.append(tmp)

                        for column_definition in column_definitions:
                            new_column = dbmanager.create_empty_column()
                            match column_definition:
                                case [col_name, col_type]:
                                    new_column["name"] = col_name
                                    new_column["type"] = col_type
                                case [col_name, col_type, "primary", "key"]:
                                    new_column = dbmanager.create_empty_column()
                                    new_column["name"] = col_name
                                    new_column["type"] = col_type
                                    new_column["primary_key"] = True
                                    new_column["allow_nulls"] = False
                                    new_table["keys"].append(f"PK__{table_name}")
                                case [col_name, col_type, "references", keypart]:
                                    pass
                                case [col_name, col_type, "constraint", constraint_name, "primary", keypart] if re.match(r"key\(" + col_name + r"\)", keypart):
                                    pass
                                case [col_name, col_type, "constraint", constraint_name, "foreign", keypart, "references", reference_column] if re.match(r"key\(" + col_name + r"\)", keypart):
                                    pass
                                case ["primary", keypart]:
                                    pass
                                case ["foreign", keypart, "references", reference_column]:
                                    pass
                                case ["constraint", constraint_name, "primary", keypart]:
                                    pass
                                case ["constraint", constraint_name, "foreign", keypart, "references", reference_column]:
                                    pass
                                case ["constraint", constraint_name, "unique", unique_column]:
                                    pass
                                # TO-DO: handle more cases (e.g.: identity property, check constraint, etc.)
                                case _:
                                    good = False
                                    break
                            if good:
                                new_table["columns"].append(new_column)
                                # TO-DO: validation
                        if good:
                            dbmanager.dbs["databases"][dbmanager.working_db]["tables"].append(new_table)
                            modified = True
                    case "index":
                        pass
                    case _:
                        good = False

            case ["drop", *obj]:
                match obj:
                    case ["database", db_name]:
                        db_idx = dbmanager.find_database(db_name);
                        if db_idx == -1:
                            response = f"Cannot drop the database '{db_name}', because it does not exist."
                            good = False
                        elif dbmanager.get_database(db_idx)["name"] == "master":
                            response = f"Cannot drop the database 'master' because it is a system database."
                            good = False
                        else:
                            del dbmanager.dbs["databases"][db_idx]
                            modified = True

                    case "table":
                        pass
                    case _:
                        good = False
            case _:
                good = False

    if not good:
        response = "Invalid command(s)\n" + response

    client_socket.send(len(response).to_bytes(4, byteorder='big'))
    client_socket.sendall(str.encode(response))

    # if there was modification in the database and there were problems, load the last stable state
    if modified and not good:
        dbmanager.dbs = dbmanager.load_databases()
    # if there was modification in the database and there were no problems, update the db file
    elif modified and good:
        dbmanager.update_databases()


def handle_client(client_socket, addr):
    while True:
        # get the commands from the client
        command_length: int = int.from_bytes(client_socket.recv(4), byteorder="big")
        commands: str = client_socket.recv(command_length).decode()
        log("Received commands:\n" + commands + "----end of commands", "logfile.txt")
        commands: list[str] = [command for command in commands.lower().split('\n') if command != '']

        if commands[0] == "exit":
            client_socket.close()
            log("Socket closed" + str(addr), "logfile.txt")
            return

        respond_to_client(client_socket, commands)


def run_server(s: socket):
    print("Server started")
    dbmanager.dbs = dbmanager.load_databases()
    print("Databases loaded")
    global stop_threads
    while not stop_threads:
        conn, addr = s.accept()
        log("Connected by" + str(addr), "logfile.txt")
        handle_client(conn, addr)


def main():
    global stop_threads
    stop_threads = False

    host = 'localhost'
    port = 12345
    s = create_socket(host, port)
    thread = Thread(target=run_server, args=[s])
    thread.start()
    input("Server running, press enter to stop!")
    stop_threads = True
    print("Stopping server...")
    # send go message to server to get it out of waiting for connection, so it can stop
    exit_socket = socket(AF_INET, SOCK_STREAM)
    exit_socket.connect((host, port))
    message = "exit"
    exit_socket.send(len(message).to_bytes(4, byteorder='big'))
    exit_socket.sendall(str.encode(message))
    exit_socket.close()
    thread.join()
    print("Server stopped")


main()

# client should send the buffer size and the data after