import dbmanager

main_commands = ["create", "drop", "alter", "insert", "select", "update", "delete", "use"]


def first_index_of_command(li: list[str]) -> int:
    # find the index of the first main_command in the list
    # return -1 if no main_command is found
    global main_commands
    for (idx, token) in enumerate(li):
        if token in main_commands:
            return idx
    return -1


def bracket_end_index(li: list[str]) -> int:
    # find the first (...) in the list and return the index of the closing bracket
    bracket_count = 0
    for (idx, token) in enumerate(li):
        if token == "(":
            bracket_count += 1
        elif token == ")":
            bracket_count -= 1
            if bracket_count == 0:
                return idx
    return -1


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


def main():
    raw_commands: str = ""
    while True:
        raw_commands += input("Enter commands: ")
        if raw_commands.endswith("#"):
            break
    tokens: list[str] = dbmanager.normalize_input(raw_commands)

    for c in extract_commands(tokens):
        print(c)


def extract_commands(tokens) -> list[list[str]]:
    commands: list[list[str]] = []
    c_idx: int = 0
    while True:
        if c_idx >= len(tokens):
            # no more tokens
            break
        if tokens[c_idx] not in main_commands:
            # command not found on current index
            print(f"Command not found: {tokens[c_idx]}")
            return []

        next_c_idx = next_index_of_command(c_idx, tokens)
        command: list[str] = tokens[c_idx:next_c_idx]
        commands.append(command)
        c_idx = next_c_idx

    return commands


def next_index_of_command(c_idx, tokens):
    next_c_idx: int = len(tokens)  # next command index set to end of tokens if no more commands
    last_idx: int = c_idx  # last command index set to the first command index
    while True:
        # find the next command index not in brackets if it exists
        current_idx: int = first_index_of_command(tokens[last_idx + 1:])
        if current_idx == -1:
            # no more commands
            break
        current_idx += last_idx + 1  # adjust index to the original list
        if not bracket_started(tokens[c_idx + 1:current_idx]):
            # if the next command is not in brackets
            # checks brackets from the first command (NOT from the last) to the current
            next_c_idx = current_idx
            break
        else:
            # if the next command is in brackets
            last_idx = current_idx
    return next_c_idx


main()
