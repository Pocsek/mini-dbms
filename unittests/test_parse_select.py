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

    def test_select_list_expressions_no_string(self):
        raw_command = "GETDATE(), 123, MAX(P.Age)"
        token_list = self.__to_token_list(raw_command)
        result = token_list.consume_group(TSelectList()).__dict__()
        expected = [{'type': 'expression', 'value': {'type': 'function', 'value': {'type': 'date_and_time', 'function': {'name': 'getdate'}}}}, {'type': 'expression', 'value': {'type': 'constant', 'value': '123'}}, {'type': 'expression', 'value': {'type': 'function', 'value': {'type': 'aggregate', 'function': {'is_distinct': False, 'name': 'max', 'column_reference': {'table': 'P', 'column': 'Age'}}}}}]
        print(json.dumps(result, indent=4))
        self.assertEqual(expected, result)

    def test_select_list_expressions_string(self):
        raw_command = "col1, 42, 'hello'"
        token_list = self.__to_token_list(raw_command)
        result = token_list.consume_group(TSelectList()).__dict__()
        expected = [{'type': 'column', 'selection': {'column_reference': {'column': 'col1'}}}, {'type': 'expression', 'value': {'type': 'constant', 'value': '42'}}, {'type': 'expression', 'value': {'type': 'constant', 'value': 'hello'}}]
        print(json.dumps(result, indent=4))
        self.assertEqual(expected, result)

    def test_table_source_derived_table(self):
        raw_command = ("(SELECT ID "
                       "FROM Citizens"
                       ") AS ids")
        token_list = self.__to_token_list(raw_command)
        result = token_list.consume_group(TTableSource()).__dict__()
        print(json.dumps(result, indent=4))

    def test_table_source_joined_table_1(self):
        raw_command = ("products p "
                       "INNER JOIN categories c ON c.category_id = p.category_id")
        token_list = self.__to_token_list(raw_command)
        result = token_list.consume_group(TTableSource()).__dict__()
        expected = {'table_type': 'joined', 'join_type': 'inner', 'left_table': {'table_type': 'database', 'table_name': 'products', 'table_alias': 'p'}, 'right_table': {'table_type': 'database', 'table_name': 'categories', 'table_alias': 'c'}, 'join_condition': [{'left': {'table': 'c', 'column': 'category_id'}, 'op': '=', 'right': {'table': 'p', 'column': 'category_id'}}]}
        print(json.dumps(result, indent=4))
        self.assertEqual(result, expected)

    def test_table_source_joined_table_2(self):
        raw_command = ("products p "
                       "INNER JOIN categories c ON c.category_id = p.category_id "
                       "JOIN brands b ON b.brand_id = p.brand_id")
        token_list = self.__to_token_list(raw_command)
        result = token_list.consume_group(TTableSource()).__dict__()
        expected = {'table_type': 'joined', 'join_type': 'inner', 'left_table': {'table_type': 'joined', 'join_type': 'inner', 'left_table': {'table_type': 'database', 'table_name': 'products', 'table_alias': 'p'}, 'right_table': {'table_type': 'database', 'table_name': 'categories', 'table_alias': 'c'}, 'join_condition': [{'left': {'table': 'c', 'column': 'category_id'}, 'op': '=', 'right': {'table': 'p', 'column': 'category_id'}}]}, 'right_table': {'table_type': 'database', 'table_name': 'brands', 'table_alias': 'b'}, 'join_condition': [{'left': {'table': 'b', 'column': 'brand_id'}, 'op': '=', 'right': {'table': 'p', 'column': 'brand_id'}}]}
        print(json.dumps(result, indent=4))
        self.assertEqual(result, expected)

    def test_select_1(self):
        raw_command = ("SELECT DISTINCT * FROM Citizens C")
        token_list = self.__to_token_list(raw_command)
        result = token_list.consume_group(TSelect(True)).__dict__()
        expected = {'is_distinct': True, 'select_list': [{'type': '*'}], 'table_source': {'table_type': 'database', 'table_name': 'Citizens', 'table_alias': 'C'}}
        print(json.dumps(result, indent=4))
        self.assertEqual(result, expected)

    def test_select_2(self):
        raw_command = ("SELECT p.product_name, c.category_name, b.brand_name, p.price "
                       "FROM products p "
                       "INNER JOIN categories c ON c.category_id = p.category_id "
                       "INNER JOIN brands b ON b.brand_id = p.brand_id")
        token_list = self.__to_token_list(raw_command)
        result = token_list.consume_group(TSelect(True)).__dict__()
        expected = {'is_distinct': False, 'select_list': [{'type': 'column', 'selection': {'column_reference': {'table': 'p', 'column': 'product_name'}}}, {'type': 'column', 'selection': {'column_reference': {'table': 'c', 'column': 'category_name'}}}, {'type': 'column', 'selection': {'column_reference': {'table': 'b', 'column': 'brand_name'}}}, {'type': 'column', 'selection': {'column_reference': {'table': 'p', 'column': 'price'}}}], 'table_source': {'table_type': 'joined', 'join_type': 'inner', 'left_table': {'table_type': 'joined', 'join_type': 'inner', 'left_table': {'table_type': 'database', 'table_name': 'products', 'table_alias': 'p'}, 'right_table': {'table_type': 'database', 'table_name': 'categories', 'table_alias': 'c'}, 'join_condition': [{'left': {'table': 'c', 'column': 'category_id'}, 'op': '=', 'right': {'table': 'p', 'column': 'category_id'}}]}, 'right_table': {'table_type': 'database', 'table_name': 'brands', 'table_alias': 'b'}, 'join_condition': [{'left': {'table': 'b', 'column': 'brand_id'}, 'op': '=', 'right': {'table': 'p', 'column': 'brand_id'}}]}}
        print(json.dumps(result, indent=4))
        self.assertEqual(result, expected)

    def test_select_3(self):
        raw_command = ("SELECT o.order_id, product_name "
                       "FROM (SELECT * "
                       "    FROM products p "
                       "    INNER JOIN categories c ON c.category_id = p.category_id "
                       "    INNER JOIN brands b ON b.brand_id = p.brand_id "
                       ") as dt "
                       "    JOIN orders o ON o.order_id = dt.order_id"
                       )
        token_list = self.__to_token_list(raw_command)
        result = token_list.consume_group(TSelect(True)).__dict__()
        expected = {'is_distinct': False, 'select_list': [{'type': 'column', 'selection': {'column_reference': {'table': 'o', 'column': 'order_id'}}}, {'type': 'column', 'selection': {'column_reference': {'column': 'product_name'}}}], 'table_source': {'table_type': 'joined', 'join_type': 'inner', 'left_table': {'table_type': 'derived', 'subquery': {'is_distinct': False, 'select_list': [{'type': '*'}], 'table_source': {'table_type': 'joined', 'join_type': 'inner', 'left_table': {'table_type': 'joined', 'join_type': 'inner', 'left_table': {'table_type': 'database', 'table_name': 'products', 'table_alias': 'p'}, 'right_table': {'table_type': 'database', 'table_name': 'categories', 'table_alias': 'c'}, 'join_condition': [{'left': {'table': 'c', 'column': 'category_id'}, 'op': '=', 'right': {'table': 'p', 'column': 'category_id'}}]}, 'right_table': {'table_type': 'database', 'table_name': 'brands', 'table_alias': 'b'}, 'join_condition': [{'left': {'table': 'b', 'column': 'brand_id'}, 'op': '=', 'right': {'table': 'p', 'column': 'brand_id'}}]}}, 'table_alias': 'dt'}, 'right_table': {'table_type': 'database', 'table_name': 'orders', 'table_alias': 'o'}, 'join_condition': [{'left': {'table': 'o', 'column': 'order_id'}, 'op': '=', 'right': {'table': 'dt', 'column': 'order_id'}}]}}
        print(json.dumps(result, indent=4))
        self.assertEqual(result, expected)

    def test_select_4(self):
        raw_command = ("SELECT DISTINCT * FROM Citizens C "
                       "WHERE C.Height < C.Weight AND C.Weight > 99 AND C.Age = 30")
        token_list = self.__to_token_list(raw_command)
        result = token_list.consume_group(TSelect(True)).__dict__()
        expected = {'is_distinct': True, 'select_list': [{'type': '*'}], 'table_source': {'table_type': 'database', 'table_name': 'Citizens', 'table_alias': 'C'}, 'search_condition': [{'left': {'table': 'C', 'column': 'Height'}, 'op': '<', 'right': {'table': 'C', 'column': 'Weight'}}, {'left': {'table': 'C', 'column': 'Weight'}, 'op': '>', 'right': 99}, {'left': {'table': 'C', 'column': 'Age'}, 'op': '=', 'right': 30}]}
        print(json.dumps(result, indent=4))
        self.assertEqual(result, expected)

    def test_select_5(self):
        raw_command = ("SELECT * FROM Citizens "
                       "WHERE Height < Weight AND Age = 30")
        token_list = self.__to_token_list(raw_command)
        result = token_list.consume_group(TSelect(True)).__dict__()
        print(json.dumps(result, indent=4))

    def test_select_6(self):
        raw_command = ("SELECT * FROM Citizens "
                       "WHERE Height <= Weight AND Age >= 30")
        token_list = self.__to_token_list(raw_command)
        result = token_list.consume_group(TSelect(True)).__dict__()
        print(json.dumps(result, indent=4))
