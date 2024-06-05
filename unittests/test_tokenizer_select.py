from unittest import TestCase
from server_side.interpreter.token_classification import TokenType
from server_side.interpreter.token_list import TokenList
from server_side.interpreter.tokenizer import Tokenizer
from server_side.interpreter.token_objects import *


class TestTokenizerSelect(TestCase):

    def test_where_1(self):
        raw_command = "WHERE Height > Weight AND Age > 21"
        token_list = TokenList(Tokenizer.tokenize(raw_command))

        token_list.consume_concrete("where")
        logic_exp = token_list.consume_group(TLogicalExpression())
        print(logic_exp.get_expressions())

    def test_where_2(self):
        raw_command = "WHERE Name = 'Jancsibacsi' AND Age < 70 AND Feleseg = 1"
        token_list = TokenList(Tokenizer.tokenize(raw_command))

        token_list.consume_concrete("where")
        logic_exp = token_list.consume_group(TLogicalExpression())
        print(logic_exp.get_expressions())
