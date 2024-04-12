class TokenType:
    MAIN_KEYWORD = 0
    SECONDARY_KEYWORDS = 1
    DATATYPE = 2
    PARENTHESIS = 3
    SEPARATOR = 4
    UNARY_OPERATOR = 5
    BINARY_OPERATOR = 6
    NUMBER = 7
    STRING = 8
    REFERENCE = 9
    # TABLE_REFERENCE = 10
    # COLUMN_REFERENCE = 11
    # RESULT_COLUMN_REFERENCE = 12  # e.g.: first row of a select command


class Literal:
    MAIN_KEYWORDS = (
        "use",
        "create",
        "drop",
        "alter",
        "insert",
        "select",
        "update",
        "delete"
    )

    SECONDARY_KEYWORDS = (
        "add",
        "as",
        "asc",
        "by",
        "check"
        "column",
        "constraint",
        "database",
        "default",
        "desc",
        "distinct",
        "exists",
        "foreign",
        "from",
        "group",
        "having",
        "inner",
        "into",
        "is",
        "join",
        "left",
        "like",
        "limit",
        "not",
        "null",
        "order",
        "outer",
        "primary",
        "right",
        "table",
        "top",
        "unique",
        "values",
        "view",
        "where"
    )

    DATATYPES = (
        "int"
        "float",
        "bit",
        "date",
        "datetime",
        "varchar"
    )

    PARENTHESES = (
        "(",
        ")",
    )

    SEPARATORS = (
        ",",
        ";"
    )

    UNARY_OPERATORS = (
        "not",
        "+",
        "-"
    )

    BINARY_OPERATORS = (
        ">",
        "<",
        "+",
        "-",
        "*",
        "/",
        "%",
        "=",
        ">=",
        "<=",
        "<>",
        "!=",
        "+=",
        "-=",
        "*=",
        "/=",
        "%=",
        "and",
        "or"
    )
