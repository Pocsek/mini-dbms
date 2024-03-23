from socket import *


def get_user_input() -> ([str], bool):
    nr: int = 0
    commands: [str] = []
    while True:
        nr += 1
        command = input(f"{nr}> ")
        commands.append(command)
        match command:
            case "go" | "GO":
                return commands, True
            case "exit" | "EXIT":
                return [], False


def main():
    s = socket(AF_INET, SOCK_STREAM)
    host = 'localhost'
    port = 12345
    s.connect((host, port))
    while True:
        commands, keep_running = get_user_input()
        if keep_running:
            if len(commands) != 0:
                for command in commands:
                    s.send(command.encode())
                data = s.recv(1024).decode()
                print(data)
        else:
            s.close()
            break


main()
