from dbmanager import DbManager
from interpreter.tree_objects.custom_tree import CustomTree
from interpreter.tree_objects.executable_tree import ExecutableTree
from interpreter.tree_objects.table_constraint_definition import TableConstraintDefinition
from .column_definition import ColumnDefinition
from database_objects import Table, Column


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
        self.__col_defs = []
        self.__table_constr_defs = []

    def validate(self, dbm: DbManager = None, mongo_client=None):
        """
        Check if there already exists a table with the given name.
        """
        pass

    def _execute(self, dbm: DbManager = None, mongo_client=None):
        """
        Update the json structure with the new table.
        """
        # columns = Column()
        # for col_def in self.__col_defs:
        #     pass

    def connect_nodes_to_root(self):
        pass

    def connect_subtrees_to_root(self):
        pass

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_column_definitions(self):
        return self.__col_defs

    def get_constraint_definitions(self):
        return self.__table_constr_defs

    def add_column_definition(self, col_def: ColumnDefinition):
        self.__col_defs.append(col_def)

    def add_table_constraint_definition(self, constr_def):
        self.__table_constr_defs.append(constr_def)
