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

        # store in a dict (<primary_key>, list[ (<column_reference>, <value>), ... ]) pairs
        self.__queried_values: dict = {}

        # save the DbManager and the working db to simplify code
        from server_side.dbmanager import DbManager
        self.__dbm: DbManager | None = None
        self.__db = None
        self.__db_idx = None

    def __setup(self, dbm):
        self.__dbm = dbm
        self.__db = self.__dbm.get_working_db()
        self.__db_idx = self.__dbm.get_working_db_index()

    def _execute(self, dbm):
        self.__process_from(dbm)
        self.__process_where(dbm)
        self.__process_select_list()
        self.__process_distinct()

        # set the result set tuple for the client to receive
        self.get_result().set_result_set((self.__result_header, self.__result_values))

    def validate(self, dbm, **kwargs):
        self.__setup(dbm)

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
         - only considers logical expressions that contain a column reference on one side and a value on the other side
         - only works with single column indexes (no composite indexes)

        Sets the attributes '__result_header' and '__result_values' only if WHERE is not specified.
        """
        # is FROM specified
        table_source_type = self.__get_table_source_type()
        if table_source_type is None:
            # table source not given
            return
        # is WHERE specified
        search_condition = self.__select_parsed.get("search_condition")
        if search_condition is None:
            # no filtering is done => load all data
            self.__load_all_values(dbm)
            return

        indexed_conditions, not_indexed_conditions = self.__split_indexed_not_indexed(search_condition)

        match table_source_type:
            case "database":
                pk_key_set = None  # this is a set that contains pk values that make a set of unique values
                if indexed_conditions:
                    # only ONE table is involved
                    # - go through each indexed condition and create a set of PKs and intersect it with the previous one
                    # - store in a dict (<primary_key>, list[ (<column_reference>, <value>), ... ]) pairs
                    # TODO group op cond_val - range query
                    for ic in indexed_conditions:
                        col_ref, col_name, table_name, op, cond_val = self.__parse_dict_expression(ic)
                        result: list[tuple] | None = self.__dbm.query_index_collection(self.__db.get_name(), table_name,
                                                                                       col_name, op, cond_val)
                        if result is None:
                            # TODO all set is empty, shouldn't continue
                            self.__queried_values = {}
                            self.__result_header = self.__tables[table_name].get_column_names()
                            self.__result_values = []
                            return
                        else:
                            pk_set = set()
                            for kv_pair in result:
                                pk_list = kv_pair[1]
                                val = kv_pair[0]
                                pk_set.update(pk_list)

                                for pk_key in pk_list:
                                    val_tp_list: list = self.__queried_values.get(pk_key, None)
                                    tupp = ({"table": table_name, "column": col_name}, val)
                                    if val_tp_list is None:
                                        self.__queried_values[pk_key] = [tupp]
                                    else:
                                        self.__queried_values[pk_key].append(tupp)

                        if pk_key_set is not None:
                            pk_key_set = pk_key_set.intersection(pk_set)
                        else:
                            pk_key_set = pk_set
                    self.__queried_values = [{qvk: self.__queried_values[qvk]} for qvk in self.__queried_values.keys() if
                                             qvk in pk_key_set]  # filter out the non-intersecting keys
                if not_indexed_conditions:
                    table_name = self.__get_table_source_name()
                    if pk_key_set is None:
                        # no indexed conditions => iterate through the entire table
                        results: list[list] = self.__dbm.find_all(self.__db.get_name(), table_name)
                    else:
                        results = self.__dbm.find_by_primary_keys(self.__db.get_name(), table_name, list(pk_key_set))
                    column_names = self.__tables[table_name].get_column_names()
                    self.__result_header = column_names
                    for res in results:
                        if self.__satisfies_conditions(res, not_indexed_conditions, column_names):
                            self.__result_values.append(res)
                    self.__queried_values = {}
            case "joined":
                raise NotImplementedError("Table joins are not supported yet")
            case "derived":
                raise NotImplementedError("Derived tables are not supported yet")

    def __find_table_by_column(self, column_name: str):
        """
        Search through every given table's columns find the table corresponding to the given column name.
        :return: database object of type Table
        """
        for table in list(self.__tables.values()):
            if table.has_index_with(column_name):
                return table
            if column_name in table.get_column_names():
                return table
        raise ValueError(f"Table with column '{column_name}' not found")

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
                right_table_source: dict = self.__select_parsed.get("table_source").get("right_table")
                if right_table_source.get("table_type") != "database":
                    raise RecursionError("Wrongly implemented JOIN, right table must be a database table")

                left_table_source: dict = self.__select_parsed.get("table_source").get("left_table")
                if left_table_source.get("table_type") != "database":
                    raise NotImplementedError("Left table must be a database table in the current implementation")

                condition: dict = self.__select_parsed["table_source"]["join_condition"][0]
                left_table_name = left_table_source.get("table_name")
                right_table_name = right_table_source.get("table_name")
                left_table = self.__tables[left_table_name]
                right_table = self.__tables[right_table_name]
                left_side = condition.get("left")
                right_side = condition.get("right")
                op = condition.get("op")
                if self.__get_name_by_alias(left_side.get("table")) == left_table_name:
                    left_table_column_name = left_side.get("column")
                    right_table_column_name = right_side.get("column")
                else:
                    left_table_column_name = right_side.get("column")
                    right_table_column_name = left_side.get("column")
                self.__result_header = left_table.get_column_names() + right_table.get_column_names()
                self.__result_values = dbm.join_tables(dbm.get_working_db_index(),
                                                       left_table,
                                                       right_table,
                                                       op,
                                                       left_table_column_name,
                                                       right_table_column_name)

                # raise NotImplementedError("Table joins are not supported yet")
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
            # determine if the column has index
            is_indexed = False
            left = expression.get("left")
            col_name = left.get("column")
            table_name = left.get("table")  # can be None
            if table_name:
                # table name is given => search through the table's indexes list
                if self.__tables[table_name].has_index_with(col_name):
                    is_indexed = True
            else:
                # table name not given => search through every given table's indexes list
                for table in list(self.__tables.values()):
                    if table.has_index_with(col_name):
                        is_indexed = True
                        break
            if is_indexed:
                indexed.append(expression)
            else:
                not_indexed.append(expression)
        return indexed, not_indexed

    def __process_select_list(self):
        """
        Updates the attributes '__result_header' and '__result_values'.
        """
        table_source_type = self.__get_table_source_type()
        if table_source_type is None:
            self.__select_list_no_table_source()
            return
        self.__select_list_database_table_source()

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
        """
        ! Current version:
            - only works for column references and '*'
        """
        select_list = self.__select_parsed.get("select_list")
        if self.__queried_values:
            raise NotImplementedError("Only indexed values in WHERE not supported")
        all_col_refs = self.__build_all_col_refs()
        proj_positions_in_all = []
        self.__result_header = []
        for projection in select_list:
            projection_type = projection.get("type")
            match projection_type:
                case "*":
                    # don't need to change the result set => can skip this step
                    return
                case "column":
                    proj_col_ref = projection.get("column_reference")
                    pos_of_ref_in_all = -1
                    for i, col_ref in enumerate(all_col_refs):
                        proj_col_name = proj_col_ref["column"]
                        if col_ref["column"] == proj_col_name:
                            table_name = proj_col_ref.get("table", None)
                            if table_name is None:
                                table_name = self.__find_table_by_column(proj_col_name).get_name()
                            if col_ref["table"] == table_name:
                                pos_of_ref_in_all = i
                    proj_col_ref_col_name = proj_col_ref.get("column")
                    if pos_of_ref_in_all == -1:
                        raise ValueError(f"Unclear column reference: {proj_col_ref_col_name}")
                    proj_positions_in_all.append(pos_of_ref_in_all)
                    self.__result_header.append(projection.get("alias", proj_col_ref_col_name))
                case "expression":
                    raise NotImplementedError("Expressions in SELECT clause are not supported yet")
        self.__result_values = [[res[pos] for pos in proj_positions_in_all] for res in self.__result_values]

    def __build_all_col_refs(self) -> list[dict]:
        col_refs = []
        for tb in self.__tables.values():
            tb_name = tb.get_name()
            references = [{"table": tb_name, "column": col_name} for col_name in tb.get_column_names()]
            col_refs.extend(references)
        return col_refs

    def __get_projected_column_references(self, select_list: list[dict]) -> list[dict]:
        col_refs = []
        for projection in select_list:
            projection_type = projection.get("type")
            match projection_type:
                case "*":
                    raise NotImplementedError("'*' in SELECT clause is not supported yet")
                case "column":
                    col_refs.append(projection.get("column_reference"))
                case "expression":
                    raise NotImplementedError("Expressions in SELECT clause are not supported yet")

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

    def __get_name_by_alias(self, alias: str) -> str:
        """If the alias is not found, return the alias itself."""
        return self.__table_aliases.get(alias, alias)

    def __parse_dict_expression(self, expression: dict) -> tuple[dict, str, str, str, any]:
        col_ref = expression.get("left")
        col_name = col_ref.get("column")
        table_name = col_ref.get("table")
        if table_name is None:
            table_name = self.__find_table_by_column(col_name).get_name()
        else:
            table_name = self.__get_name_by_alias(table_name)  # resolve alias
        op = expression.get("op")
        cond_val = expression.get("right")
        return col_ref, col_name, table_name, op, cond_val

    def __satisfies_conditions(self, res: list, conditions: list[dict], column_names: list[str]):
        for condition in conditions:
            col_ref, col_name, table_name, op, cond_val = self.__parse_dict_expression(condition)
            idx = column_names.index(col_name)
            val = res[idx]
            if not datatypes.eval_logical_expression(val, op, cond_val):
                return False
        return True



