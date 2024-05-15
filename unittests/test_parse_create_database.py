from unittest import TestCase
from server_side.interpreter.parser import Parser
from server_side.interpreter.tree_objects import CreateDatabase


class TestParseCreateDatabase(TestCase):

    def setUp(self):
        self.parser = Parser()

    def test1(self):
        raw_command = "create database test_db"
        self.parser.parse(raw_command)
        ast_list = self.parser.get_ast_list()
        self.assertEqual(len(ast_list), 1)
        self.assertIsInstance(ast_list[0], CreateDatabase)
        self.assertEqual(ast_list[0].get_name().get_value(), "test_db")