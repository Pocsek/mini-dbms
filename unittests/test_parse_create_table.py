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
        self.assertIsInstance(ast_list[0].get_column_definitions()[0].get_col_constraints()[0].get_constraint_type(), PrimaryKey)

    def test_foreign_key(self):
        raw_command = "create table test_table (col1 int, foreign key (col1) references other_table(col1))"
        self.parser.parse(raw_command)
        ast_list = self.parser.get_ast_list()
        self.assertEqual(len(ast_list), 1)
        self.assertIsInstance(ast_list[0], CreateTable)
        self.assertEqual(ast_list[0].get_name(), "test_table")
        self.assertEqual(len(ast_list[0].get_column_definitions()), 1)
        self.assertEqual(ast_list[0].get_column_definitions()[0].get_name(), "col1")
        self.assertEqual(ast_list[0].get_column_definitions()[0].get_datatype(), "int")
        self.assertEqual(len(ast_list[0].get_constraint_definitions()), 1)
        self.assertEqual(ast_list[0].get_constraint_definitions()[0].get_column_name(), "col1")
        self.assertEqual(ast_list[0].get_constraint_definitions()[0].get_referenced_table(), "other_table")
        self.assertEqual(ast_list[0].get_constraint_definitions()[0].get_referenced_column(), "col1")

    def test_empty_command(self):
        raw_command = ""
        self.parser.parse(raw_command)
        ast_list = self.parser.get_ast_list()
        self.assertEqual(len(ast_list), 0)
