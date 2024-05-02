from socket import *
from threading import Thread
from datetime import datetime

from dbmanager import *
from interpreter import *


stop_threads = False


# dbm = DbManager()  # create an instance of the DbManager class, loads the databases from the file too


def log(message: str):
    filename = "logfile.txt"
    f = open(filename, "a")
    time = datetime.now()
    f.write(str(time) + " -- " + message + '\n')
    f.close()


def create_socket(host, port) -> socket:
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((host, port))
    sock.listen()
    return sock


# def respond_to_client(client_socket: socket, commands: str):
#     global dbm
#     good: bool = True
#     modified: bool = False
#     response: str = ""
#
#     commands: list[str] = tokenize_input(commands)
#     log("Normalized commands:\n" + " ".join(commands))
#     # print(commands)
#     match commands:
#         case ["use", obj]:
#             db_idx = dbm.find_database(obj)
#             if db_idx == -1:
#                 response = f"Database '{obj}' does not exist. Make sure that the name is entered correctly."
#                 good = False
#             else:
#                 response = f"Changed database context to '{obj}'."
#                 dbm.set_working_db_index(db_idx)
#
#         case ["create", *obj]:
#             match obj:
#                 # example command: create database test1
#                 case ["database", db_name]:
#                     db_idx = dbm.find_database(db_name)
#                     if db_idx != -1:
#                         response = f"Database '{db_name}' already exists. Choose a different database name."
#                         good = False
#                     else:
#                         dbm.set_working_db_index(len(dbm.get_databases()))
#                         new_db: Database = Database(name=db_name)
#                         dbm.add_database(new_db)
#                         modified = True
#
#                 # example command: create table t1 ( ... )
#                 case ["table", table_name, "(", *column_commands, ")"]:
#                     new_table: Table = Table(name=table_name)
#
#                     column_definitions = []
#                     tmp = []
#                     for word in column_commands:
#                         if word[-1] == ',':
#                             tmp.append(word[:-1])
#                             column_definitions.append(tmp)
#                             tmp = []
#                         else:
#                             tmp.append(word)
#                     column_definitions.append(tmp)
#
#                     for column_definition in column_definitions:
#                         new_column: Column = create_empty_column()
#                         match column_definition:
#                             case [col_name, col_type]:
#                                 new_column.set_name(col_name)
#                                 new_column.set_type(col_type)
#                             case [col_name, col_type, "primary", "key"]:
#                                 # new_column["name"] = col_name
#                                 # new_column["type"] = col_type
#                                 # new_column["allow_nulls"] = False
#                                 # new_table["keys"]["primary_key"].append(col_name)
#                                 pass
#                             case [col_name, col_type, "references", keypart]:
#                                 pass
#                             case [col_name, col_type, "constraint", constraint_name, "primary",
#                                   keypart] if re.match(r"key\(" + col_name + r"\)", keypart):
#                                 pass
#                             case [col_name, col_type, "constraint", constraint_name, "foreign", keypart,
#                                   "references", reference_column] if re.match(r"key\(" + col_name + r"\)", keypart):
#                                 pass
#                             case ["primary", keypart]:
#                                 pass
#                             case ["foreign", keypart, "references", reference_column]:
#                                 pass
#                             case ["constraint", constraint_name, "primary", keypart]:
#                                 pass
#                             case ["constraint", constraint_name, "foreign", keypart, "references",
#                                   reference_column]:
#                                 pass
#                             case ["constraint", constraint_name, "unique", unique_column]:
#                                 pass
#                             # TO-DO: handle more cases (e.g.: identity property, check constraint, etc.)
#                             case _:
#                                 good = False
#                                 break
#                         if good:
#                             new_table["columns"].append(new_column)
#                             # TO-DO: validity checks
#                     if good:
#                         # TO-DO: validity checks
#                         dbm.get_working_db().add_table(new_table)
#                         modified = True
#                 case ["index", name, "on", tb, "(", *columns, ")"]:
#                     # TO-DO: add unique indexes (create unique index)
#                     # TO-DO: maybe check if the current name for the index already exists or not
#                     new_index: Index = Index(name=name)
#                     table_idx = dbm.find_table(dbm.get_working_db_index(), tb)
#                     if table_idx != -1:
#                         # if table exists
#                         if all(col in dbm.get_column_names(dbm.get_working_db_index(), table_idx)
#                                for col in columns):
#                             # if all columns exist
#                             new_index.set_columns(columns)
#                         else:
#                             good = False
#                             response += f"Column(s) not found in table '{tb}'\n"
#                     else:
#                         good = False
#                         response += (f"Table '{tb}' not found in database "
#                                      f"'{dbm.get_working_db().get_name()}'\n")
#
#                     if good:
#                         dbm.get_working_db().get_tables()[table_idx].add_index(new_index)
#                         modified = True
#                         response += f"Added '{name}' index\n"
#
#                 case _:
#                     good = False
#
#         case ["drop", *obj]:
#             match obj:
#                 case ["database", db_name]:
#                     db_idx = dbm.find_database(db_name)
#                     if db_idx == -1:
#                         response = f"Cannot drop the database '{db_name}', because it does not exist."
#                         good = False
#                     elif dbm.get_databases()[db_idx].get_name() == "master":
#                         response = f"Cannot drop the database 'master' because it is a system database."
#                         good = False
#                     else:
#                         del dbm.get_databases()[db_idx]
#                         modified = True
#
#                 case ["table", table_name]:
#                     db_idx = dbm.get_working_db_index()
#                     table_idx = dbm.find_table(db_idx, table_name)
#                     if table_idx == -1:
#                         response = f"Cannot drop the table '{table_name}', because it does not exist."
#                         good = False
#                     else:
#                         del dbm.get_databases()[db_idx].get_tables()[table_idx]
#                         # TO-DO: delete corresponding file containing table data
#                         modified = True
#                 case _:
#                     good = False
#         case _:
#             good = False
#
#     if not good:
#         response = "Invalid command(s)\n" + response
#
#     client_socket.send(len(response).to_bytes(4, byteorder='big'))
#     client_socket.sendall(str.encode(response))
#
#     # if there was modification in the database and there were problems, load the last stable state
#     if modified and not good:
#         dbm.load_databases()
#     # if there was modification in the database and there were no problems, update the db file
#     elif modified and good:
#         dbm.update_databases()


def respond_to_client(client_socket: socket, commands: str):
    # global dbm
    # good: bool = True
    # modified: bool = False
    response: str = ""

    try:
        ast_list = Parser.parse(commands)  # list of abstract syntax trees (one ast for each independent command block)
        # Executor.execute(ast_list, dbm)  # execute every syntax tree
    except Exception as e:
        response = f"Error: {e.__str__()}"

    client_socket.send(len(response).to_bytes(4, byteorder='big'))
    client_socket.sendall(str.encode(response))

    # if there was modification in the database and there were problems, load the last stable state
    # if modified and not good:
    #     dbm.load_databases()
    # if there was modification in the database and there were no problems, update the db file
    # elif modified and good:
    #     dbm.update_databases()


def handle_client(client_socket, addr):
    """
    Handles the client connection and the commands received from the client socket. It will keep the connection open
    until the client sends the "exit" command.
    """
    while True:
        # get the commands from the client
        command_length: int = int.from_bytes(client_socket.recv(4), byteorder="big")
        commands: str = client_socket.recv(command_length).decode()
        log("Received commands:\n" + commands + "----end of commands")
        if commands == "exit":
            client_socket.close()
            log("Socket closed" + str(addr))
            return
        respond_to_client(client_socket, commands)


def run_server(s: socket):
    log("Server started")
    print("Server running, press enter to stop!")
    # dbmanager.dbs = dbmanager.load_databases()
    # log("Databases loaded")
    global stop_threads
    while not stop_threads:
        conn, addr = s.accept()
        log("Connected by" + str(addr))
        handle_client(conn, addr)


def main():
    global stop_threads
    stop_threads = False

    host = 'localhost'
    port = 12345
    s = create_socket(host, port)
    thread = Thread(target=run_server, args=[s])
    thread.start()
    input("")
    stop_threads = True
    log("Stopping server...")
    # send go message to server to get it out of waiting for connection, so it can stop
    exit_socket = socket(AF_INET, SOCK_STREAM)
    exit_socket.connect((host, port))
    message = "exit"
    exit_socket.send(len(message).to_bytes(4, byteorder='big'))
    exit_socket.sendall(str.encode(message))
    exit_socket.close()
    thread.join()
    log("Server stopped")


main()

# client should send the buffer size and the data after
