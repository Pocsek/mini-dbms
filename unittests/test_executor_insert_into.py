from unittest import TestCase

import pymongo.errors

from server_side.interpreter.parser import Parser
from server_side.interpreter.executor import Executor
from server_side.dbmanager import DbManager
from server_side.interpreter.token_classification import TokenType
from server_side.interpreter.token_objects import *


class TestExecutorInsertInto(TestCase):

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
             "  col2 int unique ,"
             "  col3 varchar"
             ");"
             "create index idx1 on test_t1(col2);")
        )
        setup = self.parser.get_ast_list()
        self.executor.execute(setup)

        self.parser.parse(
            "insert into test_t1 values (1, 2, 'Pistabacsi'), (2, 4, 'Marikaneni'), (3, 3, 'Kiskutya')"
        )
        insert = self.parser.get_ast_list()
        self.executor.execute(insert)

        self.parser.parse("drop database test_db")
        cleanup = self.parser.get_ast_list()
        # self.executor.execute(cleanup)

    def test_multiple_same_primary_key(self):
        try:
            self.parser.parse(
                ("drop database if exists test_db;"
                 "create database test_db;"
                 "use test_db;"
                 "create table test_t1 ("
                 "  col1 int primary key,"
                 ");")
            )
            setup = self.parser.get_ast_list()
            self.executor.execute(setup)

            self.parser.parse(
                "insert into test_t1 values (123), (123)"
            )
            insert = self.parser.get_ast_list()

            # assure that a ValueError exception is raised DURING the insert into PK integrity validation
            with self.assertRaises(ValueError) as context:
                self.executor.execute(insert)
            self.assertIn("primary key", str(context.exception).lower())

            # assure that the exception was not raised during the insertion into MongoDB
            self.assertNotIsInstance(context.exception.__context__, pymongo.errors.DuplicateKeyError)

        finally:
            self.parser.parse("drop database if exists test_db")
            cleanup = self.parser.get_ast_list()
            self.executor.execute(cleanup)

    def test_multiple_same_unique_key_int(self):
        try:
            self.parser.parse(
                ("drop database if exists test_db;"
                 "create database test_db;"
                 "use test_db;"
                 "create table test_t1 ("
                 "  col1 int primary key,"
                 "  col2 int unique"
                 ");")
            )
            setup = self.parser.get_ast_list()
            self.executor.execute(setup)

            self.parser.parse(
                "insert into test_t1 values (1, 123), (2, 123)"
            )
            insert = self.parser.get_ast_list()

            # assure that an ValueError is raised, i.e. there is a unique key violation
            with self.assertRaises(ValueError) as context:
                self.executor.execute(insert)
            self.assertIn("unique key", str(context.exception).lower())
        finally:
            self.parser.parse("drop database if exists test_db")
            cleanup = self.parser.get_ast_list()
            self.executor.execute(cleanup)

    def test_multiple_same_unique_key_varchar(self):
        try:
            self.parser.parse(
                ("drop database if exists test_db;"
                 "create database test_db;"
                 "use test_db;"
                 "create table test_t1 ("
                 "  col1 int primary key,"
                 "  col2 varchar unique"
                 ");")
            )
            setup = self.parser.get_ast_list()
            self.executor.execute(setup)

            self.parser.parse(
                "insert into test_t1 values (1, 'Pistabacsi'), (2, 'Pistabacsi')"
            )
            insert = self.parser.get_ast_list()

            # assure that an ValueError is raised, i.e. there is a unique key violation
            with self.assertRaises(ValueError) as context:
                self.executor.execute(insert)
            self.assertIn("unique key", str(context.exception).lower())
        finally:
            self.parser.parse("drop database if exists test_db")
            cleanup = self.parser.get_ast_list()
            self.executor.execute(cleanup)

    def test_consecutive(self):
        try:
            self.parser.parse(
                ("drop database if exists test_db;"
                 "create database test_db;"
                 "use test_db;"
                 "create table test_t1 ("
                 "  col1 int primary key,"
                 "  col2 varchar unique"
                 ");")
            )
            setup = self.parser.get_ast_list()
            self.executor.execute(setup)

            self.parser.parse(
                "insert into test_t1 values (1, 'Pistabacsi');"
                "insert into test_t1 values (2, 'Pistabacsi');"
            )
            insert = self.parser.get_ast_list()

            # assure that an ValueError is raised, i.e. there is a unique key violation
            with self.assertRaises(ValueError) as context:
                self.executor.execute(insert)
            self.assertIn("unique key", str(context.exception).lower())

        finally:
            self.parser.parse("drop database if exists test_db")
            cleanup = self.parser.get_ast_list()
            self.executor.execute(cleanup)

