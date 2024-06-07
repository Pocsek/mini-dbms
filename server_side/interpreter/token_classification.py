class TokenType:
    MAIN_KEYWORD = "Main Keyword"
    KEYWORD = "Keyword"
    DATATYPE = "Datatype"
    PARENTHESIS = "Parenthesis"
    SEPARATOR = "Separator"
    UNARY_OPERATOR = "Unary Operator"
    BINARY_OPERATOR = "Binary Operator"
    LOGICAL_OPERATOR = "Logical Operator"
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
        "avg",
        "by",
        "cascade",
        "check",
        "column",
        "count",
        "constraint",
        "database",
        "default",
        "desc",
        "distinct",
        "exists",
        "foreign",
        "from",
        "getdate",
        "group",
        "having",
        "identity",
        "if",
        "index",
        "inner",
        "into",
        "is",
        "join",
        "left",
        "like",
        "limit",
        "on",
        "min",
        "max",
        "no",
        "not",
        "null",
        "order",
        "outer",
        "primary",
        "references",
        "right",
        "set",
        "sum",
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

    LOGICAL_OPERATORS = (
        ">",
        "<",
        "=",
        ">=",
        "<=",
        "<>",
        "!="
        "and",
        "or"
    )
