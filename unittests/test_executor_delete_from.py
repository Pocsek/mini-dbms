from unittest import TestCase
from server_side.interpreter.parser import Parser
from server_side.interpreter.executor import Executor
from server_side.dbmanager import DbManager
from server_side.interpreter.token_classification import TokenType
from server_side.interpreter.token_objects import *


class TestExecutorDeleteFrom(TestCase):

    def setUp(self):
        self.parser = Parser()
        self.dbm = DbManager()
        self.executor = Executor(self.dbm)

    def test_1(self):
        self.parser.parse(
            ("drop database if exists test_db;"
             "create database test_db;"
             "use test_db;"
             "create table test_t1 ("
             "  col1 int primary key,"
             "  col2 int,"
             "  col3 varchar"
             ");")
        )
        setup = self.parser.get_ast_list()
        self.executor.execute(setup)

        self.parser.parse(
            "insert into test_t1 values (1, 2, 'Pistabacsi'), (2, 2, 'Marikaneni')"
        )
        insert = self.parser.get_ast_list()
        self.executor.execute(insert)

        self.parser.parse(
            "delete from test_t1 where col1 = 1"
        )
        delete = self.parser.get_ast_list()
        self.executor.execute(delete)

        self.parser.parse("drop database test_db")
        cleanup = self.parser.get_ast_list()
        # self.executor.execute(cleanup)

    def test_with_indexes(self):
        self.parser.parse(
            ("drop database if exists test_db;"
             "create database test_db;"
             "use test_db;"
             "create table test_t1 ("
             "  col1 int primary key,"
             "  col2 int,"
             "  col3 varchar"
             ");"
             "create index idx1 on test_t1(col2);")
        )
        setup = self.parser.get_ast_list()
        self.executor.execute(setup)

        self.parser.parse(
            "insert into test_t1 values (1, 2, 'Pistabacsi'), (2, 4, 'Marikaneni'), (3, 2, 'Kiskutya')"
        )
        insert = self.parser.get_ast_list()
        self.executor.execute(insert)

        self.parser.parse(
            "delete from test_t1 where col1 = 1"
        )
        delete = self.parser.get_ast_list()
        # self.executor.execute(delete)

        self.parser.parse("drop database test_db")
        cleanup = self.parser.get_ast_list()
        # self.executor.execute(cleanup)

