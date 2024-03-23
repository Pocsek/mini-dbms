from socket import *
from threading import Thread
from datetime import datetime

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
    good: bool = False
    # do something with the commands
    for command in commands:
        match command.lower().strip().split():
            case ["create", obj]:
                match obj:
                    case "table":
                        good = True
                    case "database":
                        good = True
                    case "index":
                        good = True
                    case _:
                        good = False
            case ["drop", obj]:
                match obj:
                    case "table":
                        good = True
                    case "database":
                        good = True
                    case _:
                        good = False
            case _:
                good = False
    if not good:
        client_socket.sendall(str.encode("invalid command(s)"))
    else:
        # this is just for testing
        client_socket.sendall(str.encode("ok"))


def handle_client(client_socket, addr):
    while True:
        commands: [str] = []
        # get the commands from the client
        while True:
            command = client_socket.recv(1024).decode()
            log("Received command: {}".format(command), "logfile.txt")
            if command == "go" or command == "GO":
                respond_to_client(client_socket, commands)
                break
            if command == "exit" or command == "EXIT":
                client_socket.close()
                log("Socket closed" + str(addr), "logfile.txt")
                return
            commands.append(command)


def run_server(s: socket):
    print("Server started")
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
    exit_socket.sendall(str.encode("exit"))
    exit_socket.close()
    thread.join()
    print("Server stopped")


main()
