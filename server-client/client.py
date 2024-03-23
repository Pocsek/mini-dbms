from socket import *


def get_user_input() -> ([str], bool):
    nr: int = 0
    commands: [str] = []
    while True:
        nr += 1
        command = input(f"{nr}> ")
        commands.append(command)
        match command.lower():
            case "go":
                return commands, True
            case "exit":
                return ["exit"], False


def main():
    s = socket(AF_INET, SOCK_STREAM)
    host = 'localhost'
    port = 12345
    s.connect((host, port))
    try:
        while True:
            commands, keep_running = get_user_input()
            if len(commands) != 0:
                for command in commands:
                    s.sendall(command.encode())
                data = s.recv(1024).decode()
                print(data)
            if not keep_running:
                s.close()
                break
    except KeyboardInterrupt:
        print("Ctrl+C pressed")


main()
