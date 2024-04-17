import json
import os
from database_objects import *


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

    # # cannot really sync databases with mongoDB, because mongoDB doesn't create the database until a collection is created
    # def sync_databases_with_mongo(self):
    #     mongo_dbs = mongo_db.get_database_names()
    #     for db in self.get_databases():
    #         if db.get_name() not in mongo_dbs:
    #             mongo_db.create_database(db.get_name())
    #         else:
    #             # TO-DO: sync tables
    #             pass
    #
    # # TO-DO: implement sync_tables_with_mongo!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # def sync_tables_with_mongo(self, db_idx):
    #     db: Database = self.get_databases()[db_idx]
    #     mongo_tables = mongo_db.get_collection_names(db.get_name())
    #     for tb in db.get_tables():
    #         if tb.get_name() not in mongo_tables:
    #             # TO-DO: create table
    #             pass

    def get_databases(self) -> list[Database]:
        return self.__dbs

    def get_working_db_index(self) -> int:
        return self.__working_db

    def set_working_db_index(self, db_idx):
        self.__working_db = db_idx

    def get_working_db(self) -> Database:
        return self.get_databases()[self.get_working_db_index()]

    def find_database(self, name: str) -> int:
        for (idx, db) in enumerate(self.get_databases()):
            if db.get_name() == name:
                return idx
        return -1

    def find_table(self, db_idx: int, table_name: str) -> int:
        for (idx, tb) in enumerate(self.get_databases()[db_idx].get_tables()):
            if tb.get_name() == table_name:
                return idx
        return -1

    def get_table_names(self, db_idx) -> list[str]:
        return [tb.get_name() for tb in self.get_databases()[db_idx].get_tables()]

    def get_column_names(self, db_idx, table_idx) -> list[str]:
        return [col.get_name() for col in self.get_databases()[db_idx].get_tables()[table_idx].get_columns()]

    def add_database(self, db: Database):
        # TO-DO: check if the database already exists
        self.__dbs.append(db)

    def insert_one(self, db: Database, tb: Table, record: dict) -> bool:
        """
        Inserts a record into a table creating a key-value pair.
        Checks if the database and table exist.
        """
        # TO-DO: provide better feedback on what went wrong
        # TO-DO: check if the record has the correct types
        db_idx = self.find_database(db.get_name())
        if db_idx == -1:
            return False
        if self.find_table(db_idx, tb.get_name()) == -1:
            return False
        column_names = tb.get_column_names()
        primary_key_names = tb.get_primary_key().get_column_names()
        if len(column_names) == 0:
            # cannot insert a record into a table with no columns
            return False
        if len(primary_key_names) == 0:
            # cannot insert a record into a table with no primary key
            return False
        key, value = build_key_value_pair(record, column_names, primary_key_names)
        return mongo_db.insert_one(db.get_name(), tb.get_name(), key, value)

    def insert_many(self, db: Database, tb: Table, records: list[dict]) -> tuple[bool, list]:
        pass

    def delete_one(self, db: Database, tb: Table, key: str) -> bool:
        """
        Deletes a record from a table.
        Checks if the database and table exist.
        """
        # TO-DO: provide better feedback on what went wrong
        # TO-DO: key should be a condition somehow and from it, I should build a dict to pass further
        db_idx = self.find_database(db.get_name())
        if db_idx == -1:
            return False
        if self.find_table(db_idx, tb.get_name()) == -1:
            return False
        return mongo_db.delete_one(db.get_name(), tb.get_name(), {"_id": key})

    def delete_many(self, db: Database, tb: Table, keys: str) -> bool:
        pass


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


def build_key_value_pair(record: dict, column_names: list[str], primary_key_names: list[str]) -> tuple[str, str]:
    """
    Build a key-value pair, from a record in a table.
    Concatenates the values of the primary key columns into the key.
    Concatenate other colum values into the value.
    Only keeps the values that belong to existing table names.
    Ignores non-existent names.
    """
    key: str = str()
    value: str = str()
    separator_char = "#"
    for col in column_names:
        part: str = f'{record.get(col,"")}{separator_char}'
        if col in primary_key_names:
            key += part
        else:
            value += part
    return key[:-1], value[:-1]  # don't add the separator character at the end
