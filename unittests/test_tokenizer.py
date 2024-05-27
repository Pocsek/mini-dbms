from unittest import TestCase
from server_side.interpreter.tokenizer import Tokenizer
from server_side.interpreter.token_list import TokenList
from server_side.interpreter.token_classification import TokenType


class TestTokenizer(TestCase):

    def setUp(self):
        pass

    def test_tokenize_with_multiple_spaces(self):
        raw_commands = "CREate   TAblE   t   (   Col1   INt   ,   Col2   flOAT   )   ;"
        tokens_all = Tokenizer.tokenize(raw_commands)
        self.assertEqual(
            tokens_all,
            ["create", "table", "t", "(", "Col1", "int", ",", "Col2", "float", ")", ";"]
        )

    def test_tokenize_with_no_spaces(self):
        raw_commands = "CREate TAblE t(Col1 INt,Col2 flOAT);"
        tokens_all = Tokenizer.tokenize(raw_commands)
        self.assertEqual(
            tokens_all,
            ["create", "table", "t", "(", "Col1", "int", ",", "Col2", "float", ")", ";"]
        )

    def test_1(self):
        raw_commands = (
            "create table t("
            "   col1 cheCK(1<(2+1))"
            ");"
            "DRop table t;"
        )
        tokens_all = Tokenizer.tokenize(raw_commands)
        self.assertEqual(
            tokens_all,
            ["create", "table", "t", "(",
                "col1", "check", "(", "1", "<", "(","2","+","1",")",")",
             ")",";",
             "drop", "table", "t",";"]
        )


