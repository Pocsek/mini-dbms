from socket import *
from threading import Thread
from datetime import datetime
import sys

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
        # the true-false logic is not correct, but it will change anyway
        match command.lower().strip().split():
            case ["use", obj]:
                # need to check whether the obj is existing
                good = True
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
        response: str = "invalid command(s)"
        client_socket.send(len(response).to_bytes(4, byteorder='big'))
        client_socket.sendall(str.encode(response))
    else:
        # this is just for testing
        response: str = "ok"
        client_socket.send(len(response).to_bytes(4, byteorder='big'))
        client_socket.sendall(str.encode(response))


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