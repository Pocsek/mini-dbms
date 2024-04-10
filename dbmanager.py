import json
import os
from typing import List

import sqlparse
import re
from database_objects import *
from database_objects import Database, Table, Index


class DbManager:
    __dbs: list[Database] = []
    __working_db = 0  # the index of the database we're currently using

    def __init__(self):
        self.load_databases()

    def load_databases(self):
        if os.path.exists("databases.json"):
            with open("databases.json", "r") as f:
                data: list[dict] = json.load(f)  # decode (JSON -> python dict)
                self.__dbs = [Database().from_dict(db) for db in data]
        else:
            with open("databases.json", "w") as f:
                self.__dbs = create_default_databases()
                json.dump([db.__dict__() for db in self.__dbs], f, indent=4)

    def update_databases(self):
        with open("databases.json", "w") as f:
            json.dump(self.__dbs, f, indent=4)  # encode (python dict -> JSON)

    def get_databases(self) -> list[Database]:
        return self.__dbs

    def get_working_db_index(self) -> int:
        return self.__working_db

    def set_working_db_index(self, db_idx):
        self.__working_db = db_idx

    def get_working_db(self) -> Database:
        return self.get_databases()[self.get_working_db_index()]

    def find_database(self, name) -> int:
        for (idx, db) in enumerate(self.get_databases()):
            if db.get_name() == name:
                return idx
        return -1

    def find_table(self, db_idx, table_name) -> int:
        for (idx, tb) in enumerate(self.get_databases()[db_idx].get_tables()):
            if tb.get_name() == table_name:
                return idx
        return -1

    def get_table_names(self, db_idx) -> list[str]:
        table_names = []
        for tb in self.get_databases()[db_idx].get_tables():
            table_names.append(tb.get_name())
        return table_names

    def get_column_names(self, db_idx, table_idx) -> list[str]:
        column_names = []
        for col in self.get_databases()[db_idx].get_tables()[table_idx].get_columns():
            column_names.append(col.get_name())
        return column_names

    def add_database(self, db: Database):
        self.__dbs.append(db)


def create_default_databases() -> list[Database]:
    return [Database(name="master")]


def create_empty_database() -> Database:
    return Database()


def create_empty_foreign_key() -> dict:
    return {
        "attributes": [],
        "references": {
            "table": "",
            "attributes": []
        }
    }


def create_empty_table() -> Table:
    return Table()


def create_empty_column() -> Column:
    return Column()


def create_empty_index() -> Index:
    return Index()


# takes a string of SQL commands and turns it into a list of strings where each keyword, operator, separator, etc. is a
# different list element -> this is an essential step to take before starting to interpret the commands
def tokenize_input(commands_string) -> list[str]:
    datatypes = ("int", "float", "bit", "date", "datetime", "varchar")
    tokenized = re.sub(r"([(),;])", r" \1 ", commands_string)  # put space around parentheses, separators
    tokenized = sqlparse.format(
        tokenized,
        keyword_case="lower", # cast keywords to lowercase (create, select, group by, or, between, etc. EXCLUDING DATATYPES like int, float, etc.)
        strip_comments=True  # remove comments (both "--" and "/* */" variants)
    )
    tokenized = re.sub(r"(>=|<=|<>|!=|\+=|-=|\*=|/=|%=)", r" \1 ", tokenized)  # put space around compound operators
    tokenized = re.sub(r"([^><+\-*/%=])(>|<|[+\-*/%@=])([^=])", r"\1 \2 \3", tokenized)  # put space around simple operators
    tokenized = tokenized.replace("\n", " ")  # concatenate all lines into one line
    tokenized = re.sub(" +", " ", tokenized)  # remove extra spaces
    tokenized = tokenized.strip()  # remove possible trailing space
    tokenized = tokenized.split(" ")  # split by spaces

    # cast datatypes to lowercase
    for i, val in enumerate(tokenized):
        val_lower = val.lower()
        if val_lower in datatypes:
            tokenized[i] = val_lower

    return tokenized
