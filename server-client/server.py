from socket import *
from threading import Thread

stop_threads = False


def create_socket(host, port) -> socket:
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((host, port))
    sock.listen()
    return sock


def handle_client(client_socket):
    commands: [str] = []
    # get the commands from the client
    while True:
        command = client_socket.recv(1024).decode()
        if command == "go" or command == "GO":
            break
        commands.append(command)
    if len(commands) != 0:
        good: bool = False
        # do something with the commands
        for command in commands:
            # this is not necessarily the best wat to do this, but will help in the future
            match command.strip().split():
                case ["create", "table"] | ["CREATE", "TABLE"]:
                    good = True
                case ["drop", "table"] | ["DROP", "TABLE"]:
                    good = True
                case ["create", "database"] | ["CREATE", "DATABASE"]:
                    good = True
                case ["drop", "database"] | ["DROP", "DATABASE"]:
                    good = True
                case ["create", "index"] | ["CREATE", "INDEX"]:
                    good = True
                case _:
                    good = False

        if not good:
            client_socket.send(str.encode("invalid statement"))
        else:
            # this is just for testing
            client_socket.send(str.encode("ok"))

    client_socket.close()


def run_server(s: socket):
    print("Server started")
    global stop_threads
    while not stop_threads:
        conn, addr = s.accept()
        print("Connected by", addr)
        handle_client(conn)


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
    exit_socket.send(str.encode("go"))
    exit_socket.close()
    thread.join()
    print("Server stopped")


main()
