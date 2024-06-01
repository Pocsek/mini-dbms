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

    def __insert_n_records_multiple_values(self, nr_records: int):
        """
        ! This function should be called from inside a test.

        Simulates inserting n records into a table by a single call to the insert command.
        Insertion is done in the following format:
            INSERT INTO <table> values  (...),
                                        (...),
                                        ..
                                        ..
                                        (...)
        """
        try:
            self.parser.parse(
                ("drop database if exists test_insert_multiple;"
                 "create database test_insert_multiple;"
                 "use test_insert_multiple;"
                 "create table customers ("
                 "  ID int primary key identity,"
                 "  Name varchar,"
                 "  Age int,"
                 "  EmailAddress varchar"
                 ");")
            )
            setup = self.parser.get_ast_list()
            self.executor.execute(setup)

            command = "insert into customers values "
            for i in range(nr_records):
                record = "('{}', {}, '{}')".format("name", 18, "email@address.com")
                command += f"{record},"

            self.parser.parse(command[:-1])  # cut off comma at the end
            insert = self.parser.get_ast_list()
            self.executor.execute(insert)
        finally:
            self.parser.parse("drop database if exists test_insert_multiple")
            cleanup = self.parser.get_ast_list()
            self.executor.execute(cleanup)

    def __insert_n_values_consecutive_calls(self, nr_records: int):
        """
        ! This function should be called from inside a test.

        Simulates inserting n records into a table by consecutive calls to the insert command.
        Insertion is done in the following format:
            INSERT INTO <table> values  (...);
            INSERT INTO <table> values  (...);
            ...
            INSERT INTO <table> values  (...);
        """
        try:
            self.parser.parse(
                ("drop database if exists test_insert_consecutive;"
                 "create database test_insert_consecutive;"
                 "use test_insert_consecutive;"
                 "create table customers ("
                 "  ID int primary key identity,"
                 "  Name varchar,"
                 "  Age int,"
                 "  EmailAddress varchar"
                 ");")
            )
            setup = self.parser.get_ast_list()
            self.executor.execute(setup)

            commands = " "
            for i in range(nr_records):
                insert_cmd = "insert into customers values ('{}', {}, '{}'); ".format("name", 18, "email@address.com")
                commands += insert_cmd

            self.parser.parse(commands)
            insert = self.parser.get_ast_list()
            self.executor.execute(insert)

        finally:
            self.parser.parse("drop database if exists test_insert_consecutive")
            cleanup = self.parser.get_ast_list()
            self.executor.execute(cleanup)

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

    def test_default_values(self):
        self.parser.parse(
            ("drop database if exists test_default_values;"
             "create database test_default_values;"
             "use test_default_values;"
             "create table t1 ("
             "  col1 int primary key,"
             "  col2 int default 10,"
             "  col3 varchar default 'something',"
             "  col4 int not null"
             ");")
        )
        setup = self.parser.get_ast_list()
        self.executor.execute(setup)

        self.parser.parse(
            "insert into t1 (col1) values (123)"
        )
        insert = self.parser.get_ast_list()
        self.executor.execute(insert)

        self.parser.parse("drop database test_default_values")
        cleanup = self.parser.get_ast_list()
        # self.executor.execute(cleanup)

    def test_check_constraint(self):
        self.parser.parse(
            ("drop database if exists test_check_constraint;"
             "create database test_check_constraint;"
             "use test_check_constraint;"
             "create table t1 ("
             "  col1 int primary key,"
             "  col2 int check (col2 > 9) not null"
             ");")
        )
        setup = self.parser.get_ast_list()
        self.executor.execute(setup)

        self.parser.parse(
            "insert into t1 values (123, 8)"
        )
        insert = self.parser.get_ast_list()
        self.executor.execute(insert)

        self.parser.parse("drop database test_default_values")
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
                "insert into test_t1 values (123), (124), (123)"
            )
            insert = self.parser.get_ast_list()

            # assure that a ValueError exception is raised DURING the insert into PK integrity validation
            with self.assertRaises(ValueError) as context:
                self.executor.execute(insert)

            # # assure that the exception was not raised during the insertion into MongoDB
            self.assertNotIsInstance(context.exception.__context__, pymongo.errors.DuplicateKeyError)

            self.assertIn("primary key", str(context.exception).lower())

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

    def test_insert_multiple_values_100(self):
        self.__insert_n_records_multiple_values(100)

    def test_insert_multiple_values_1000(self):
        self.__insert_n_records_multiple_values(1000)

    def test_insert_multiple_values_10000(self):
        self.__insert_n_records_multiple_values(10000)

    def test_insert_consecutive_100(self):
        self.__insert_n_values_consecutive_calls(100)

    def test_insert_consecutive_1000(self):
        self.__insert_n_values_consecutive_calls(1000)

    def test_insert_consecutive_10000(self):
        self.__insert_n_values_consecutive_calls(10000)
