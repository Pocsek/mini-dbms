from unittest import TestCase
from server_side.interpreter.parser import Parser
from server_side.interpreter.token_classification import TokenType
from server_side.interpreter.token_objects import *


class TestParser(TestCase):

    def setUp(self):
        self.parser = Parser()

    def test_parse_invalid_command(self):
        raw_command = "invalid command"
        with self.assertRaises(SyntaxError):
            self.parser.parse(raw_command)

    def test_parse_empty_command(self):
        raw_command = ""
        self.parser.parse(raw_command)
        ast_list = self.parser.get_ast_list()
        self.assertEqual(len(ast_list), 0)
