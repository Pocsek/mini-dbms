from socket import *


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
        # the exit and go commands won't make it into the commands string
        if command != "":
            commands += command + "\n"


def main():
    s = socket(AF_INET, SOCK_STREAM)
    host = 'localhost'
    port = 12345
    s.connect((host, port))
    try:
        while True:
            commands, keep_running = get_user_input()
            command_length: int = len(commands)
            if command_length != 0:
                s.sendall(command_length.to_bytes(4, byteorder="big"))  # send buffer size
                s.sendall(commands.encode())  # send commands
                if keep_running:
                    response_length: int = int.from_bytes(s.recv(4), byteorder="big")
                    response = s.recv(response_length).decode()
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
