from server_side.interpreter.tree_objects.executable_tree import ExecutableTree


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
        column_alias
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
            The order of table sources after the FROM keyword doesn't affect the result set that is returned.
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
        column_alias
            An optional alias to replace a column name in the result set of the derived table. Include one column alias
            for each column in the select list, and enclose the complete list of column aliases in parentheses.
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

            When the condition specifies columns, the columns don't have to have the same name or same data type;
            however, if the data types aren't the same, they must be either compatible or types that SQL Server can
            implicitly convert.

    References:
        https://learn.microsoft.com/en-us/sql/t-sql/queries/select-transact-sql?view=sql-server-ver16
        https://learn.microsoft.com/en-us/sql/t-sql/queries/select-clause-transact-sql?view=sql-server-ver16
        https://learn.microsoft.com/en-us/sql/t-sql/queries/from-transact-sql?view=sql-server-ver16
    """

    def __init__(self, select_token):
        """
        :param select_token: instance of TSelect that has already consumed a SELECT clause
        """
        super().__init__()
        self.__select_token = select_token.__dict__()

    def _execute(self, dbm):
        pass

    def validate(self, dbm, **kwargs):
        pass

    def __repr__(self):
        return self.__select_token
