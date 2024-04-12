import dbmanager

# list of main commands which are used to separate commands
main_commands = ["create", "drop", "alter", "insert", "select", "update", "delete", "use"]


def first_index_of_command(li: list[str]) -> int:
    # find the index of the first main_command in the list
    # return -1 if no main_command is found
    global main_commands
    for (idx, token) in enumerate(li):
        if token in main_commands:
            return idx
    return -1


def next_index_of_command(start_c_idx, tokens):
    # find the index of the next main_command in the list which is not in brackets
    next_c_idx: int = len(tokens)  # next command index set to end of tokens if no more commands
    last_idx: int = start_c_idx  # last command index set to the start command index
    while True:
        # find the next command index not in brackets if it exists
        current_idx: int = first_index_of_command(tokens[last_idx + 1:])
        if current_idx == -1:
            # no more commands
            break
        current_idx += last_idx + 1  # adjust index to the original list
        if not bracket_started(tokens[start_c_idx + 1:current_idx]):
            # if the next command is not in brackets
            # checks brackets from the first command (NOT from the last) to the current
            next_c_idx = current_idx
            break
        else:
            # if the next command is in brackets
            last_idx = current_idx
    return next_c_idx


def bracket_started(li: list[str]) -> bool:
    # check if a bracket has started but not closed
    bracket_count = 0
    for token in li:
        if token == "(":
            bracket_count += 1
        elif token == ")":
            bracket_count -= 1
            if bracket_count < 0:
                # closing bracket before opening bracket
                return False
    return bracket_count > 0


def extract_commands(tokens) -> list[list[str]]:
    # separates commands based on main_commands
    # a command is a list of tokens
    # returns a list of commands
    commands: list[list[str]] = []
    c_idx: int = 0  # current command start index
    while True:
        if c_idx >= len(tokens):
            # no more tokens
            break
        if tokens[c_idx] not in main_commands:
            # command not found on current index
            print(f"Command not found: {tokens[c_idx]}")
            return []
        # next command index is either the end of tokens or the next command index
        next_c_idx = next_index_of_command(c_idx, tokens)

        command: list[str] = tokens[c_idx:next_c_idx]
        commands.append(command)
        c_idx = next_c_idx

    return commands


# this snippet is copied from client.py -> get_user_input()
def get_input():
    # read from command line while the input does not end with "go"
    nr: int = 0
    commands: str = ""
    while True:
        nr += 1
        command = input(f"{nr}> ").strip()
        match command.lower():
            case "go":
                return commands[:-1]  # return commands string without trailing newline character
        # the exit and go commands won't make it into the commands string
        if command != "":
            commands += command + "\n"


def main():
    raw_commands = get_input()

    tokens: list[str] = dbmanager.tokenize_input(raw_commands)  # tokenize input

    # extract commands from tokens and print them
    for c in extract_commands(tokens):
        print(c)


main()
