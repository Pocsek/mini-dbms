from unittest import TestCase
from server_side.interpreter.parser import Parser
from server_side.interpreter.tree_objects import CreateTable
from server_side.interpreter.constraint_objects import *


class TestParseCreateTable(TestCase):

    def setUp(self):
        self.parser = Parser()

    def test_single_column(self):
        raw_command = "create table test_table (col1 int)"
        self.parser.parse(raw_command)
        ast_list = self.parser.get_ast_list()
        self.assertEqual(len(ast_list), 1)
        self.assertIsInstance(ast_list[0], CreateTable)
        self.assertEqual(ast_list[0].get_name(), "test_table")
        self.assertEqual(len(ast_list[0].get_column_definitions()), 1)
        self.assertEqual(ast_list[0].get_column_definitions()[0].get_name(), "col1")
        self.assertEqual(ast_list[0].get_column_definitions()[0].get_datatype(), "int")

    def test_multiple_columns(self):
        raw_command = "create table test_table (col1 int, col2 float)"
        self.parser.parse(raw_command)
        ast_list = self.parser.get_ast_list()
        self.assertEqual(len(ast_list), 1)
        self.assertIsInstance(ast_list[0], CreateTable)
        self.assertEqual(ast_list[0].get_name(), "test_table")
        self.assertEqual(len(ast_list[0].get_column_definitions()), 2)
        self.assertEqual(ast_list[0].get_column_definitions()[0].get_name(), "col1")
        self.assertEqual(ast_list[0].get_column_definitions()[0].get_datatype(), "int")
        self.assertEqual(ast_list[0].get_column_definitions()[1].get_name(), "col2")
        self.assertEqual(ast_list[0].get_column_definitions()[1].get_datatype(), "float")

    def test_primary_key(self):
        raw_command = "create table test_table (col1 int primary key)"
        self.parser.parse(raw_command)
        ast_list = self.parser.get_ast_list()
        self.assertEqual(len(ast_list), 1)
        self.assertIsInstance(ast_list[0], CreateTable)
        self.assertEqual(ast_list[0].get_name(), "test_table")
        self.assertEqual(len(ast_list[0].get_column_definitions()), 1)
        self.assertEqual(ast_list[0].get_column_definitions()[0].get_name(), "col1")
        self.assertEqual(ast_list[0].get_column_definitions()[0].get_datatype(), "int")
        self.assertIsInstance(ast_list[0].get_column_definitions()[0].get_col_constraints()[0], PrimaryKey)
        self.assertEqual(ast_list[0].get_column_definitions()[0].get_col_constraints()[0].get_column_names(), ["col1"])

    def test_foreign_key(self):
        raw_command = "create table test_table (col1 int foreign key references test_table2(col2))"
        self.parser.parse(raw_command)
        ast_list = self.parser.get_ast_list()
        self.assertEqual(len(ast_list), 1)
        self.assertIsInstance(ast_list[0], CreateTable)
        self.assertEqual(ast_list[0].get_name(), "test_table")
        self.assertEqual(len(ast_list[0].get_column_definitions()), 1)
        self.assertEqual(ast_list[0].get_column_definitions()[0].get_name(), "col1")
        self.assertEqual(ast_list[0].get_column_definitions()[0].get_datatype(), "int")
        self.assertIsInstance(ast_list[0].get_column_definitions()[0].get_col_constraints()[0], ForeignKey)
        self.assertEqual(ast_list[0].get_column_definitions()[0].get_col_constraints()[0].get_source_column_names(),
                         ["col1"])
        self.assertEqual(ast_list[0].get_column_definitions()[0].get_col_constraints()[0].get_referenced_table_name(), "test_table2")
        self.assertEqual(ast_list[0].get_column_definitions()[0].get_col_constraints()[0].get_referenced_column_names(), ["col2"])

    def test_unique(self):
        raw_command = "create table test_table (col1 int unique)"
        self.parser.parse(raw_command)
        ast_list = self.parser.get_ast_list()
        self.assertEqual(len(ast_list), 1)
        self.assertIsInstance(ast_list[0], CreateTable)
        self.assertEqual(ast_list[0].get_name(), "test_table")
        self.assertEqual(len(ast_list[0].get_column_definitions()), 1)
        self.assertEqual(ast_list[0].get_column_definitions()[0].get_name(), "col1")
        self.assertEqual(ast_list[0].get_column_definitions()[0].get_datatype(), "int")
        self.assertIsInstance(ast_list[0].get_column_definitions()[0].get_col_constraints()[0], Unique)
        self.assertEqual(ast_list[0].get_column_definitions()[0].get_col_constraints()[0].get_column_names(), ["col1"])

    def test_identity1(self):
        raw_command = "create table test_table (col1 int identity)"
        self.parser.parse(raw_command)
        ast = self.parser.get_ast_list()[0]
        self.assertIsInstance(ast.get_column_definitions()[0].get_col_constraints()[0], Identity)
        self.assertEqual(ast.get_column_definitions()[0].get_col_constraints()[0].get_seed(), 1)
        self.assertEqual(ast.get_column_definitions()[0].get_col_constraints()[0].get_increment(), 1)

    def test_identity2(self):
        raw_command = "create table test_table (col1 int identity(3,2))"
        self.parser.parse(raw_command)
        ast = self.parser.get_ast_list()[0]
        self.assertIsInstance(ast.get_column_definitions()[0].get_col_constraints()[0], Identity)
        self.assertEqual(ast.get_column_definitions()[0].get_col_constraints()[0].get_seed(), 3)
        self.assertEqual(ast.get_column_definitions()[0].get_col_constraints()[0].get_increment(), 2)

    def test_null(self):
        raw_command = "create table test_table (col1 int null)"
        self.parser.parse(raw_command)
        ast = self.parser.get_ast_list()[0]
        self.assertIsInstance(ast.get_column_definitions()[0].get_col_constraints()[0], Null)
        self.assertEqual(ast.get_column_definitions()[0].get_col_constraints()[0].get_column_name(), "col1")

    def test_not_null(self):
        raw_command = "create table test_table (col1 int not null)"
        self.parser.parse(raw_command)
        ast = self.parser.get_ast_list()[0]
        self.assertIsInstance(ast.get_column_definitions()[0].get_col_constraints()[0], NotNull)
        self.assertEqual(ast.get_column_definitions()[0].get_col_constraints()[0].get_column_name(), "col1")

    def test_default(self):
        raw_command = "create table test_table (col1 int default 1)"
        self.parser.parse(raw_command)
        ast = self.parser.get_ast_list()[0]
        self.assertIsInstance(ast.get_column_definitions()[0].get_col_constraints()[0], Default)
        self.assertEqual(ast.get_column_definitions()[0].get_col_constraints()[0].get_default_value(), 1)
