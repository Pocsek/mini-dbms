class TokenType:
    MAIN_KEYWORD = "Main Keyword"
    KEYWORD = "Keyword"
    DATATYPE = "Datatype"
    PARENTHESIS = "Parenthesis"
    SEPARATOR = "Separator"
    UNARY_OPERATOR = "Unary Operator"
    BINARY_OPERATOR = "Binary Operator"
    NUM_CONST = "Numeric Constant"
    CHAR_CONST = "Character Constant"
    IDENTIFIER = "Identifier"


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

    KEYWORDS = (
        "action",
        "add",
        "as",
        "asc",
        "by",
        "cascade",
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
        "identity",
        "index",
        "inner",
        "into",
        "is",
        "join",
        "left",
        "like",
        "limit",
        "no",
        "not",
        "null",
        "order",
        "outer",
        "primary",
        "references",
        "right",
        "set",
        "table",
        "top",
        "unique",
        "values",
        "view",
        "where"
    )

    DATATYPES = (
        "int",
        "float",
        "bit",
        "date",
        "datetime",
        "varchar"
    )

    PARENTHESES = (
        "(",
        ")"
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
