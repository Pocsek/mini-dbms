from unittest import TestCase
from server_side.interpreter.parser import Parser
from server_side.interpreter.executor import Executor
from server_side.dbmanager import DbManager
from server_side.interpreter.token_classification import TokenType
from server_side.interpreter.token_objects import *


class TestExecutorCreateDeleteTable(TestCase):

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
             ");"
             "create table test_t2 ("
             "  col1 int primary key,"
             "  col2 int,"
             "  col3 varchar"
             ")")
        )
        setup = self.parser.get_ast_list()
        self.executor.execute(setup)

        self.parser.parse(
            "drop table test_t1"
        )
        drop = self.parser.get_ast_list()
        self.executor.execute(drop)

        # self.parser.parse("drop database test_db")
        # cleanup = self.parser.get_ast_list()
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
             "create table test_t2 ("
             "  col1 int primary key,"
             "  col2 int,"
             "  col3 varchar"
             ")")
        )
        setup = self.parser.get_ast_list()
        self.executor.execute(setup)

        self.parser.parse(
            ("create index idx1 on test_t1 (col2);"
             "create index idx2 on test_t1 (col3);"
             "create index idx3 on test_t2 (col2);"
             "create index idx4 on test_t2 (col3)"
             )
        )
        indexes = self.parser.get_ast_list()
        self.executor.execute(indexes)

        self.parser.parse(
            "drop table test_t1"
        )
        drop = self.parser.get_ast_list()
        self.executor.execute(drop)

        # self.parser.parse("drop database test_db")
        # cleanup = self.parser.get_ast_list()
        # self.executor.execute(cleanup)


