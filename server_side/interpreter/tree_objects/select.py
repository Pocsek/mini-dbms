from server_side.interpreter.tree_objects.executable_tree import ExecutableTree
from server_side.interpreter import datatypes
from datetime import datetime


class Select(ExecutableTree):
    """
    Syntax:
        SELECT [DISTINCT] <select_list>
        [FROM <table_source>]
        [WHERE <search_condition>]
        [GROUP BY <group_by_expression>]

    Arguments (implementation details; see TObj subclasses for more syntax specification, e.g.: TSelectList)
        DISTINCT
            Specifies that only unique rows can appear in the result set. Null values are considered equal for the
            purposes of the DISTINCT keyword.
        <select_list>
            The columns to be selected for the result set. The select list is a series of expressions separated by
            commas.
        *
            Specifies that all columns from all tables in the FROM clause should be returned. The columns are returned
            by table, as specified in the FROM clause, and in the order in which they exist in the table.
        column_name
            Is the name of a column to return. Qualify column_name to prevent an ambiguous reference, such as occurs
            when two tables in the FROM clause have columns with duplicate names. For example, the SalesOrderHeader and
            SalesOrderDetail tables in the AdventureWorks2022 database both have a column named ModifiedDate. If the
            two tables are joined in a query, the modified date of the SalesOrderDetail entries can be specified in the
            select list as SalesOrderDetail.ModifiedDate.
        expression
            Is a constant, any combination of column names, constants, or a subquery.
        column_alias (context: select_list)
            Is an alternative name to replace the column name in the query result set. For example, an alias such as
            Quantity, or Quantity to Date, or Qty can be specified for a column named quantity.

            Aliases are used also to specify names for the results of expressions, for example:
                USE AdventureWorks2022;
                GO
                SELECT AVG(UnitPrice) AS [Average Price]
                FROM Sales.SalesOrderDetail;

            column_alias cannot be used in a WHERE, GROUP BY, or HAVING clause.
        <table_source>
            Specifies a table, or derived table source, with or without an alias, to use in the statement.
        [AS] table_alias
            An alias for table_source that can be used either for convenience or to distinguish a table or view in a
            self-join or subquery. An alias is frequently a shortened table name used to refer to specific columns of
            the tables in a join. If the same column name exists in more than one table in the join, SQL Server may
            require that the column name is qualified by a table name, view name, or alias to distinguish these columns.
            The table name can't be used if an alias is defined.

            When a derived table is used, the required table_alias at the end of the clause is the associated table name
            for all columns, including grouping columns, returned.
        derived_table
            A subquery that retrieves rows from the database. derived_table is used as input to the outer query.
        column_alias (context: derived_table)
            An optional alias to replace a column name in the result set of the derived table. Include one column alias
            for each column in the select list.
        <joined table>
            A joined table is a result set that is the product of two or more tables.
        <join type>
            Specifies the type of join operation.

            INNER
                Specifies all matching pairs of rows are returned. Discards unmatched rows from both tables. When no
                join type is specified, this is the default.
        ON <search_condition>
            Specifies the condition on which the join is based. The condition can specify any predicate, although
            columns and comparison operators are frequently used.

            When the condition specifies columns, the columns don't have to have the same name.

    References:
        https://learn.microsoft.com/en-us/sql/t-sql/queries/select-transact-sql?view=sql-server-ver16
        https://learn.microsoft.com/en-us/sql/t-sql/queries/select-clause-transact-sql?view=sql-server-ver16
        https://learn.microsoft.com/en-us/sql/t-sql/queries/from-transact-sql?view=sql-server-ver16
    """

    def __init__(self, select_parsed):
        """
        :param select_parsed: instance of TSelect that has already consumed a SELECT command
        """
        super().__init__()
        self.__select_parsed = select_parsed.__dict__()

        # the result set's header and values: represents the current state of this command's result set
        self.__result_header: list[str] = []
        self.__result_values: list[list] = []

        # hold all table aliases in one place [key=<alias>, value=<table_name>]
        self.__table_aliases: dict = {}

        # hold all table structures in one place [key=<table_name>, value=<table_dbo>]
        self.__tables: dict = {}

    def _execute(self, dbm):
        self.__process_from(dbm)
        self.__process_where(dbm)
        self.__process_select_list(dbm)
        self.__process_distinct()

        # set the result set tuple for the client to receive
        self.get_result().set_result_set((self.__result_header, self.__result_values))

    def validate(self, dbm, **kwargs):
        pass

    def __repr__(self):
        return self.__select_parsed

    def __process_from(self, dbm):
        """
        Goes through all tables of the root table source recursively.
        Sets the attributes '__table_aliases', '__tables'.
        """
        table_source = self.__select_parsed.get("table_source")
        self.__process_table_source(dbm, table_source)

    def __process_table_source(self, dbm, table_source: dict):
        """
        Goes through all tables of the current table source recursively.
        Sets the attributes '__table_aliases', '__tables'.

        :param table_source: the current table source in the recursion tree
        """
        if table_source is None:
            return
        table_type: str = table_source.get("table_type")  # cannot be None
        match table_type:
            case "database":
                table_name: str = table_source.get("table_name")
                table_alias: str = table_source.get("table_alias")  # can be None
                if table_alias:
                    self.__table_aliases[table_alias] = table_name
                self.__tables[table_name] = dbm.get_table(dbm.get_working_db_index(), table_name)
            case "joined":
                left: dict = table_source.get("left_table")
                right: dict = table_source.get("right_table")
                self.__process_table_source(dbm, left)
                self.__process_table_source(dbm, right)
            case "derived":
                raise NotImplementedError("Derived tables inside FROM clause not supported yet")

    def __process_where(self, dbm):
        """
        Performs filtering on the tables according to the search condition by creating a result set for each expression
        containing indexed columns, then intersecting them, and filtering the obtained result set with the remaining
        expressions which do not contain indexed columns.
        If none of the expressions contain indexed columns, then iterate through the entire table.

        ! Current implementation:
         - only considers logical expressions that contain a column reference one side and a value on the other side
         - only works with single column indexes (no composite indexes)

        Sets the attributes '__result_header' and '__result_values'.
        """
        search_condition = self.__select_parsed.get("search_condition")
        if search_condition is None:
            # no filtering is done => load all data
            self.__load_all_values(dbm)
            return
        indexed, not_indexed = self.__split_indexed_not_indexed(search_condition)
        indexed_result_sets: list[tuple[list[str], list]] = self.__filter_indexed(dbm, indexed)


    def __filter_indexed(self, dbm, expressions: list[dict]) -> list[tuple[list[str], list]]:
        """
        Filters indexed records in the table source.

        ! Currently, only works for conditions in the format: <column> <op> <value>

        :param expressions: a list of expressions where each contains an indexed column, a value, and a logical operator
        :return: a list of tuples where a tuple consists of its corresponding result set's header and the result set's
                values
        """
        result_sets: list[tuple[list[str], list]] = []

        for expr in expressions:
            left = expression.get("left")
            op = expr.get("op")
            right = expression.get("right")

            # for now
            if right.get("column") or not left.get("column"):
                raise NotImplementedError(
                    f"Unsupported condition format: {left} {op} {right}. Should be <column> <op> <value>."
                )

            cur_result_header = None
            left_table = None
            left_table_alias = None
            left_table_name = left.get("table")  # can be None
            left_col_name = left.get("column")
            if left_table_name is None:
                cur_result_header = [left_col_name]
                left_table = self.__find_table_by_indexed_column(dbm, left_col_name)
            else:
                # resolve the potential table alias to its real name
                alias = self.__table_aliases.get(left_table_name)
                if alias:
                    cur_result_header = [alias]
                    left_table_name = alias
                else:
                    cur_result_header = [left_table_name]
                # get the table
                left_table = dbm.get_table(dbm.get_working_db_index(), left_table_name)
            left_col_type = left_table.get_column(left_col_name).get_type()

            right_val = datatypes.cast_value(right, left_col_type)

            cur_result_values = dbm.find_conditional_indexed_by_value(
                dbm.get_working_db().get_name(),
                left_table_name,
                left_col_name,
                left_col_type,
                op,
                right_val
            )
            # save current results
            result_values_column = []
            for val in cur_result_values:
                result_values_column.append(val)
            result_sets.append((cur_result_header, result_values_column))

        return result_sets

    def __find_table_by_indexed_column(self, dbm, column_name: str):
        """
        Search through every given table's indexes list to find the table corresponding to the given column name.
        :return: database object of type Table
        """
        for table in list(self.__tables.values()):
            if table.has_index_with(column_name):
                return table
        raise ValueError(f"Table with indexed column '{column_name}' not found")

    def __load_all_values(self, dbm):
        """
        Sets the attribute '__result_header' and '__result_values' by loading all values from the table source.
        """
        table_source_type = self.__get_table_source_type()
        if table_source_type is None:
            # table source not given
            return
        match table_source_type:
            case "database":
                # load all data in the table directly from the database
                table = self.__tables[self.__get_table_source_name()]
                self.__result_header = table.get_column_names()
                self.__result_values = dbm.find_all(dbm.get_working_db().get_name(), table.get_name())
            case "joined":
                raise NotImplementedError("Table joins are not supported yet")
            case "derived":
                raise NotImplementedError("Derived tables are not supported yet")

    def __split_indexed_not_indexed(self, search_condition: list) -> tuple[list, list]:
        """
        Split a list of expressions into two lists: one that contains only indexed columns and one that contains not
        indexed columns.
        """
        indexed: list[dict] = []
        not_indexed: list[dict] = []
        for expression in search_condition:
            is_indexed = True
            left = expression.get("left")
            right = expression.get("right")
            for side in [left, right]:
                if side.get("column") is None:
                    # side is a constant
                    continue
                # side is a column reference
                col_name = left.get("column")
                table_name = left.get("table")  # can be None
                if table_name:
                    # table name is given => search through the table's indexes list
                    if self.__tables[table_name].has_index_with(col_name):
                        is_indexed = is_indexed and True  # if once it was False, it should remain False
                    else:
                        is_indexed = False
                else:
                    # table name not given => search through every given table's indexes list
                    found = False
                    for table in list(self.__tables.values()):
                        if table.has_index_with(col_name):
                            is_indexed = is_indexed and True
                            found = True
                    if not found:
                        is_indexed = False
            if is_indexed:
                indexed.append(expression)
            else:
                not_indexed.append(expression)
        return indexed, not_indexed

    def __eval_logical_expression(self, left, op, right) -> bool:
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

    def __process_select_list(self, dbm):
        """
        Updates the attributes '__result_header' and '__result_values'.
        """
        table_source_type = self.__get_table_source_type()
        if table_source_type is None:
            self.__select_list_no_table_source()
            return
        self.__select_list_database_table_source()

        match table_source_type:
            case "database":
                raise NotImplementedError("'SELECT' with 'FROM' clause not implemented")
            case "joined":
                raise NotImplementedError("Table joins are not supported yet")
            case "derived":
                raise NotImplementedError("Derived tables are not supported yet")

    def __select_list_no_table_source(self):
        """
        Special case when there is no table source given.
        """
        select_list = self.__select_parsed.get("select_list")
        self.__result_header = []
        self.__result_values = []
        record = []
        for projection in select_list:
            # only expressions can appear here
            record.append(self.__eval_value_expression(projection.get("value")))
            alias = projection.get("alias")
            if alias:
                self.__result_header.append(alias)
            else:
                self.__result_header.append("")
        self.__result_values.append(record)

    def __select_list_database_table_source(self):
        select_list = self.__select_parsed.get("select_list")
        for projection in select_list:
            self.__process_projection(projection)

    def __process_projection(self, projection: dict):
        """"""
        # TODO: implement projection after filtering is implemented
        proj_type = projection.get("type")
        raise NotImplementedError("Projection not implemented")

    def __eval_value_expression(self, expression: dict):
        """
        Evaluate an expression that has a return type of value.
        :param expression:
                {
                    "type": ("constant" | "aggregate" | "subquery"),
                    "value": <constant> | <aggregate_function> | <subquery>
                }
        :return: The result of the expression.
        """
        expr_value = expression.get("value")
        match expression.get("type"):
            case "constant":
                return expr_value
            case "function":
                return self.__eval_function(expr_value)
            case "subquery":
                raise NotImplementedError("Subqueries are not supported yet")

    def __eval_function(self, function: dict):
        """
        Evaluate a function.
        :param function:
                {
                "type": ("aggregate" | "date_and_time"),
                "function": <function>
            }
        :return: The result of the functino.
        """
        func_type = function.get("type")
        func = function.get("function")
        func_name = func.get("name")
        match func_type:
            case "date_and_time":
                match func_name:
                    case "getdate":
                        return str(datetime.now())
                    case _:
                        raise NotImplementedError(f"Date&Time function '{func_name}' not supported")
            case "aggregate":
                match func_name:
                    case "count":
                        raise NotImplementedError(f"Aggregate function '{func_name}' not supported")
                    case "sum":
                        raise NotImplementedError(f"Aggregate function '{func_name}' not supported")
                    case "avg":
                        raise NotImplementedError(f"Aggregate function '{func_name}' not supported")
                    case "min":
                        raise NotImplementedError(f"Aggregate function '{func_name}' not supported")
                    case "max":
                        raise NotImplementedError(f"Aggregate function '{func_name}' not supported")
                    case _:
                        raise NotImplementedError(f"Aggregate function '{func_name}' not supported")
            case _:
                raise NotImplementedError(f"Function of type '{func_type}' not supported")

    def __get_table_source_type(self) -> str | None:
        table_source = self.__select_parsed.get("table_source")
        if table_source:
            return table_source.get("table_type")
        return None

    def __get_table_source_name(self) -> str | None:
        table_source = self.__select_parsed.get("table_source")
        if table_source:
            return table_source.get("table_name")
        return None

    def __process_distinct(self):
        """
        Filter duplicates in the result values.
        """
        if self.__select_parsed.get("is_distinct"):
            raise NotImplementedError("DISTINCT not supported yet")
