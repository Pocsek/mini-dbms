from unittest import TestCase
from server_side.interpreter.parser import Parser
from server_side.interpreter.tree_objects import Select


class TestParseSelect(TestCase):

    def setUp(self):
        self.parser = Parser()

    def test_select_list_1(self):
        raw_command = "select col1, 42, 'hello'"
        self.parser.parse(raw_command)
        # ast = self.parser.get_ast_list()[0]

