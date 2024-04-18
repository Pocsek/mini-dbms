class TokenType:
    MAIN_KEYWORD = "Main Keyword"
    SECONDARY_KEYWORD = "Secondary Keyword"
    DATATYPE = "Datatype"
    PARENTHESIS = "Parenthesis"
    SEPARATOR = "Separator"
    UNARY_OPERATOR = "Unary Operator"
    BINARY_OPERATOR = "Binary Operator"
    NUM_CONST = "Numeric Constant"
    CHAR_CONST = "Character Constant"
    IDENTIFIER = "Identifier"
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

    OTHER_KEYWORDS = (
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
        "index",
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
