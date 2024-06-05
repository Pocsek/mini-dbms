from server_side.interpreter.tree_objects.executable_tree import ExecutableTree
from server_side.interpreter.tree_objects.column_definition import ColumnDefinition
from server_side.interpreter.constraint_objects import CObj, PrimaryKey, ForeignKey, Unique


class CreateTable(ExecutableTree):
    def __init__(self):
        """
        In a CREATE TABLE statement, a constraint can be defined at the column level or at the table level.

        At the column level, a constraint is defined as part of a column definition, and is applied only to that column.
        At the table level, a constraint is defined as a table constraint, and can be applied to more than one column.

        Examples:
            1.
            CREATE TABLE Products (
                ProductID INT PRIMARY KEY,
                Price FLOAT
            )

            2.
            CREATE TABLE Products (
                ProductID INT CONSTRAINT PK_Products PRIMARY KEY,
                Price FLOAT
            )

            3.
            CREATE TABLE Products (
                ProductID INT,
                Price FLOAT,
                CONSTRAINT PK_Products PRIMARY KEY (ProductID)
            )

            4.
            CREATE TABLE Products (
                ProductID INT,
                Price FLOAT,
                CONSTRAINT PK_Products PRIMARY KEY (ProductID, Price)
            )

            5.
            CREATE TABLE Prices (
                ID INT PRIMARY KEY,
                Price FLOAT UNIQUE
            )

            CREATE TABLE Products (
                ProductID INT PRIMARY KEY,
                Price FLOAT REFERENCES Prices(Price)
            )

            6.
            CREATE TABLE Products (
                ProductID INT PRIMARY KEY,
                Price FLOAT FOREIGN KEY REFERENCES Prices(Price) ON DELETE CASCADE NOT NULL
            )

            7.
            CREATE TABLE Products (
                ProductID INT PRIMARY KEY,
                Price FLOAT CONSTRAINT FK_Price_Products_Prices FOREIGN KEY REFERENCES Prices(Price)
            )

            8.
            CREATE TABLE Products (
                ProductID INT PRIMARY KEY,
                Price FLOAT,
                CONSTRAINT FK_Price_Products_Prices FOREIGN KEY (Price) REFERENCES Prices(Price)
            )

            9.
            CREATE TABLE Products (
                ProductID INT PRIMARY KEY,
                Price FLOAT DEFAULT 1.0 NULL CHECK (Price > 0) UNIQUE
            )
        """
        super().__init__()
        self.__name = ""
        self.__col_defs: list[ColumnDefinition] = []
        self.__table_constraints: list[CObj] = []

    def validate(self, dbm, **kwargs):
        """
        Check if there already exists a table with the given name.
        Call the validate method of the column definitions.
        Call the validate method of the table constraint definitions.
        """
        db = dbm.get_working_db()
        if db.get_table(self.__name):
            raise ValueError(f"Table with name '{self.__name}' already exists.")
        for col_def in self.__col_defs:
            col_def.validate(dbm,
                             column_definitions=self.__col_defs,
                             table_constraints=self.__table_constraints)
        for constr in self.__table_constraints:
            constr.validate(dbm,
                            column_definitions=self.__col_defs,
                            table_constraints=self.__table_constraints)

    def _execute(self, dbm):
        """
        Update the json structure with the new table.
        """
        from server_side.database_objects import Table, Column
        table = Table()
        table.set_name(self.__name)
        for col_def in self.__col_defs:
            # create column, add it to the table
            column = Column(name=col_def.get_name(), data_type=col_def.get_datatype())
            table.add_column(column)
            # add key constraints to the table
            for key in col_def.get_keys():
                table.add_key(key)
            # add other constraints to the table
            for constr in col_def.get_constraints():
                table.add_constraint(constr)
        for constr in self.__table_constraints:
            # add constraint to the table
            if _is_key(constr):
                table.add_key(constr)
            else:
                table.add_constraint(constr)

        dbm.create_table(table)
        resp_message = f"Table '{table.get_name()}' created successfully."
        self.get_result().set_response_message(resp_message)
        print(resp_message)

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_column_definitions(self):
        return self.__col_defs

    def get_constraint_definitions(self):
        return self.__table_constraints

    def add_column_definition(self, col_def: ColumnDefinition):
        self.__col_defs.append(col_def)

    def add_table_constraint(self, constr_def):
        self.__table_constraints.append(constr_def)


def _is_key(constraint: CObj):
    return isinstance(constraint, PrimaryKey) or isinstance(constraint, ForeignKey) or isinstance(constraint, Unique)
