from unittest import TestCase
from server_side.interpreter.parser import Parser
from server_side.interpreter.tree_objects import Select
from server_side.interpreter.tokenizer import Tokenizer
from server_side.interpreter.token_list import TokenList
from server_side.interpreter.token_objects import *
import json


class TestParseSelect(TestCase):

    def setUp(self):
        self.parser = Parser()

    def __to_token_list(self, raw_command):
        tokens = Tokenizer.tokenize(raw_command)
        return TokenList(tokens)

    def test_select_list_column_references(self):
        raw_command = "t.col1, col2 as ColTwo"
        token_list = self.__to_token_list(raw_command)
        result = token_list.consume_group(TSelectList()).__dict__()
        print(json.dumps(result, indent=4))

    def test_select_list_(self):
        raw_command = "col1, 42, 'hello'"
        token_list = self.__to_token_list(raw_command)
        result = token_list.consume_group(TSelectList()).__dict__()
        print(json.dumps(result, indent=4))

