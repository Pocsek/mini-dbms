from socket import *
from threading import Thread
from datetime import datetime
import traceback

from server_side.dbmanager import *
from server_side.interpreter import *
from server_side import __working_dir__


stop_threads = False


dbm = DbManager()  # create an instance of the DbManager class, loads the databases from the file too
ps = Parser()
ex = Executor(dbm)


def log(message: str):
    filename = "logfile.txt"
    f_path = os.path.join(__working_dir__, filename)
    f = open(f_path, "a")
    time = datetime.now()
    f.write(str(time) + " -- " + message + '\n')
    f.close()


def create_socket(host, port) -> socket:
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((host, port))
    sock.listen()
    return sock


def respond_to_client(client_socket: socket, commands: str):
    """
    Responds to the client with the result of the commands received.
    """
    global dbm
    global ps
    global ex
    response: str = ""

    try:
        ps.parse(commands)
        ex.execute(ps.get_ast_list())

    except Exception as e:
        response = f"Error: {e.__str__()}"
        traceback.print_exc()  # only for debugging, if error traceback is needed
        print("Error: " + e.__str__())  # this should be logged in a file in the future
        log("Error: " + e.__str__())
        # if the database was modified, load the last stable state
        if ex.modified():
            # load last stable state of the working DB
            pass

    client_socket.send(len(response).to_bytes(4, byteorder='big'))
    client_socket.sendall(str.encode(response))


def handle_client(client_socket, addr):
    """
    Handles the client connection and the commands received from the client socket. It will keep the connection open
    until the client sends the "exit" command.
    """
    global dbm
    while True:
        command_length: int = int.from_bytes(client_socket.recv(4), byteorder="big")
        commands: str = client_socket.recv(command_length).decode()
        log("Received commands:\n" + commands + "----end of commands")
        match commands:
            case "exit":
                client_socket.close()
                log("Socket closed" + str(addr))
                return
            case "show databases":
                # return the names of the databases separated by a space
                databases: list[str] = dbm.get_database_names()
                response: str = " ".join(databases)
                client_socket.send(len(response).to_bytes(4, byteorder='big'))
                client_socket.sendall(str.encode(response))
                continue
            case "show tables":
                # return the names of the tables in the working database separated by a space
                tables: list[str] = dbm.get_table_names(dbm.get_working_db_index())
                response: str = " ".join(tables)
                print(response)
                client_socket.send(len(response).to_bytes(4, byteorder='big'))
                client_socket.sendall(str.encode(response))
                continue
            case "~show structure~":
                structure: dict = dbm.__dict__()
                json_structure: str = json.dumps(structure, indent=4)
                client_socket.send(len(json_structure).to_bytes(4, byteorder='big'))
                client_socket.sendall(str.encode(json_structure))
                continue
        respond_to_client(client_socket, commands)


def run_server(s: socket):
    log("Server started")
    print("Server running, press enter to stop!")
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
