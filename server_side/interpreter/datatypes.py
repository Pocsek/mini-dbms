def matches_column_type(val, column) -> bool:
    """
    Check if the value matches the type of the column.
    """
    col_type = column.get_type()
    match col_type:
        case "int":
            return val.isdigit()
        case "float":
            return isinstance(val, float)
        case "varchar":
            return isinstance(val, str)
        case _:
            raise ValueError(f"Unknown datatype '{col_type}'.")


def cast_value(val, target_type: str):
    """Convert a value to the given type and return it."""
    match target_type:
        case "int":
            return int(val)
        case "float":
            return float(val)
        case "varchar":
            return val
        case _:
            raise ValueError(f"Unknown datatype '{target_type}'.")


def eval_logical_expression(left, op, right) -> bool:
    if type(left) != type(right):
        raise ValueError(f"Type of '{left}' differs from type of '{right}'")
    match op:
        case "<":
            return left < right
        case ">":
            return left > right
        case "<=":
            return left <= right
        case ">=":
            return left >= right
        case "=":
            return left == right
        case _:
            raise NotImplementedError(f"Invalid operator'{op}'")
