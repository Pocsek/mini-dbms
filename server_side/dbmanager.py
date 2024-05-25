import json
import os

from server_side.database_objects import Database, Table, Column, Index, PrimaryKey, ForeignKey, mongo_db
from server_side import __working_dir__


class DbManager:
    __dbs: list[Database] = []
    __working_db = 0  # the index of the database we're currently using
    # the file where the database sceleton is stored:
    __db_file: str = os.path.join(__working_dir__, "databases.json")

    def __init__(self):
        self.load_databases()

    def __dict__(self) -> dict:
        return {
            "databases": [db.__dict__() for db in self.__dbs],
            "working_db": self.__working_db
        }

    def load_databases(self):
        if os.path.exists(self.__db_file):
            with open(self.__db_file, "r") as f:
                data: list[dict] = json.load(f)  # decode (JSON -> python dict)
                self.__dbs = [Database().from_dict(db) for db in data]
        else:
            with open(self.__db_file, "w") as f:
                self.__dbs = create_default_databases()
                json.dump([db.__dict__() for db in self.__dbs], f, indent=4)

    def update_db_structure_file(self):
        with open(self.__db_file, "w") as f:
            json.dump([db.__dict__() for db in self.__dbs], f, indent=4)

    def create_table(self, table: Table):
        # create collection in MongoDB
        mongo_db.create_collection(self.get_working_db().get_name(), table.get_name())

        # update structure file
        self.get_working_db().add_table(table)
        self.update_db_structure_file()

    def create_index(self, index: Index, table_name: str):
        table: Table = self.get_table(self.get_working_db_index(), table_name)
        pr_key_names: list[str] = table.get_primary_key().get_column_names()
        column_names: list[str] = table.get_column_names()

        # create a collection with concatenated table name and index name that starts with an '__'
        coll_name: str = "__" + table_name + '#' + index.get_name()  # collection name
        mongo_db.create_collection(self.get_working_db().get_name(), coll_name)
        selection: dict = {}
        # projection: dict = {name: 1 for name in index.get_column_names()}
        # projection.update({"_id": 1})
        kv_pairs: list[dict] = mongo_db.select(self.get_working_db().get_name(), table_name, selection)

        records: list[dict] = []
        for kv_pair in kv_pairs:  # rebuild records from key-value pairs
            records.append(split_key_value_pair(kv_pair, column_names, pr_key_names))

        index_column_names: list[str] = index.get_column_names()
        used_column_names = index_column_names + pr_key_names  # columns that are used in the index

        idx_kv_pairs: list[tuple[str, str]] = []
        for record in records:
            key, value = build_key_value_pair(record, used_column_names, index_column_names)
            idx_kv_pairs.append((key, value))

        if not table.is_unique(index_column_names):  # if the column names are not unique concatenate repeating values
            idx_kv_pairs = concatenate_repeating(idx_kv_pairs)

        # insert the key-value pairs into the index collection
        for key_value_pair in idx_kv_pairs:
            try:
                mongo_db.insert_one(self.get_working_db().get_name(), coll_name, key_value_pair)
            except ValueError:
                raise

        # update structure file
        table.add_index(index)
        self.update_db_structure_file()

    def drop_database(self, db_name):
        # delete db in MongoDB
        mongo_db.drop_database(db_name)

        # update json structure
        self.__dbs.pop(self.get_db_index(db_name))
        self.update_db_structure_file()

    def drop_table(self, table_name):
        # delete collection in MongoDB
        mongo_db.drop_collection(self.get_working_db().get_name(), table_name)

        # update json structure
        db = self.get_working_db()
        db.remove_table(table_name)
        self.update_db_structure_file()

    def get_default_database_names(self) -> list[str]:
        return [db.get_name() for db in create_default_databases()]

    def get_databases(self) -> list[Database]:
        return self.__dbs

    def get_db_index(self, db_name):
        for (idx, db) in enumerate(self.__dbs):
            if db.get_name() == db_name:
                return idx

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

    def get_table(self, db_idx: int, table_name: str) -> Table | None:
        for tb in self.get_databases()[db_idx].get_tables():
            if tb.get_name() == table_name:
                return tb
        return None

    def get_database_names(self) -> list[str]:
        return [db.get_name() for db in self.get_databases()]

    def get_table_names(self, db_idx) -> list[str]:
        return [tb.get_name() for tb in self.get_databases()[db_idx].get_tables()]

    def get_column_names(self, db_idx, table_idx) -> list[str]:
        return [col.get_name() for col in self.get_databases()[db_idx].get_tables()[table_idx].get_columns()]

    def add_database(self, db: Database):
        # TO-DO: check if the database already exists
        self.__dbs.append(db)

    def insert(self, db: Database, tb: Table, records: list[dict]) -> list[str]:
        """
        Inserts records into a table creating key-value pairs.
        Checks if the database and table exist.
        !Right now it inserts only one record at a time and if it fails it raises an exception,
        but keeps the ones inserted before and ignores the rest.!
        """
        # TO-DO: check if the record has the correct types
        db_idx = self.find_database(db.get_name())
        if db_idx == -1:
            raise ValueError(f"Database [{db.get_name()}] not found")
        if self.find_table(db_idx, tb.get_name()) == -1:
            raise ValueError(f"Table [{tb.get_name()}] not found")
        column_names = tb.get_column_names()
        pr = tb.get_primary_key()
        if not pr:
            raise ValueError(f"Table [{tb.get_name()}] has no primary key")
        primary_key_names = pr.get_column_names()
        if len(column_names) == 0:
            # cannot insert a record into a table with no columns
            raise ValueError(f"Table [{tb.get_name()}] has no columns")
        if len(records) == 0:
            # cannot insert an empty record
            raise ValueError("Record is empty")
        key_value_pairs = []
        for record in records:
            key, value = build_key_value_pair(record, column_names, primary_key_names)
            key_value_pairs.append((key, value))
        inserted_keys = []
        for key_value_pair in key_value_pairs:
            try:
                inserted_keys.append(mongo_db.insert_one(db.get_name(), tb.get_name(), key_value_pair))
            except ValueError:
                raise
        return inserted_keys
        # TO-DO: implement insert_many
        # else:
        #     try:
        #         return mongo_db.insert_many(db.get_name(), tb.get_name(), key_value_pairs)
        #     except ValueError:
        #         raise

    def delete(self, db: Database, tb: Table, key: str) -> int:
        """
        Deletes records from a table.
        Checks if the database and table exist.
        Returns the number of deleted records.

        Currently, only deletes by primary-key.
        """
        # TO-DO: provide better feedback on what went wrong
        # TO-DO: key should be a condition somehow and from it, I should build a dict to pass further
        db_idx = self.find_database(db.get_name())
        if db_idx == -1:
            raise ValueError(f"Database [{db.get_name()}] not found")
        tb_idx = self.find_table(db_idx, tb.get_name())
        if tb_idx == -1:
            raise ValueError(f"Table [{tb.get_name()}] not found")
        tb = self.get_databases()[db_idx].get_tables()[tb_idx]
        if not tb.has_primary_key():  # check if the table has a primary key because we can only delete by primary key
            raise ValueError(f"Table [{tb.get_name()}] has no primary key")
        return mongo_db.delete(db.get_name(), tb.get_name(), {"_id": key})

    def find_value(self, db: Database, table: Table, column_names: list[str], value: str) -> str | None:
        """
        Find a value in a table.
        The value parameter is a string created by the concatenation of attribute values. The attribute values
        correspond to the given column names.
        Separator character between (attribute) values inside of a record is '#'.
        Separator character between values is '$'. TODO: discuss this

        :return: a string: the primary key corresponding to the value if the given value exists, else None
        """
        index = table.get_index_by_column_names(column_names)
        if index:
            # for both single and compound values only if there is an index created on all columns, use those to search
            for kv in mongo_db.select(db.get_name(), index.get_name()):
                key_part, value_part = kv.get("_id"), kv.get("value")
                if key_part == value:
                    # non-unique column(s) -> return string containing concatenated primary keys for this value
                    return value_part
                else:
                    # unique column(s) -> look for the given value in the value part of the key-value pair
                    for v in value_part.split("$"):
                        if v == value:
                            return key_part
        else:
            # else iterate through the collection (table)
            for kv in mongo_db.select(db.get_name(), table.get_name()):
                if kv.get("value") == value:
                    return kv.get("_id")
        return None


def create_default_databases() -> list[Database]:
    return [Database(name="master")]


def create_empty_database() -> Database:
    return Database()


def create_empty_foreign_key() -> ForeignKey:
    return ForeignKey()


def create_empty_table() -> Table:
    return Table()


def create_empty_column() -> Column:
    return Column()


def create_empty_index() -> Index:
    return Index()


def create_empty_primary_key() -> PrimaryKey:
    return PrimaryKey()


def build_key_value_pair(record: dict, all_names: list[str], key_names: list[str]) -> tuple[str, str]:
    """
    Build a key-value pair, from a record in a table.
    Concatenates the values of the primary key columns into the key.
    Concatenate other colum values into the value.
    Only keeps the values that belong to existing table names.
    Ignores non-existent names.
    Separator character is "#".
    """
    key: str = str()
    value: str = str()
    separator_char = "#"
    for name in all_names:
        part: str = f'{record.get(name, "")}{separator_char}'
        if name in key_names:
            key += part
        else:
            value += part
    return key[:-1], value[:-1]  # don't add the separator character at the end


def split_key_value_pair(key_value_pair: dict, all_names: list[str], key_names: list[str]) -> dict:
    """
    Split a key-value pair into a record.
    Splits by the separator character "#".
    """
    record: dict = {}
    separator_char = "#"
    key: str = key_value_pair.get("_id", "")
    value: str = key_value_pair.get("value", "")
    key_parts: list[str] = key.split(separator_char)
    value_parts: list[str] = value.split(separator_char)
    for col in all_names:
        if col in key_names:
            record[col] = key_parts.pop(0)
        else:
            record[col] = value_parts.pop(0)
    return record


def concatenate_repeating(kv_pairs: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """
    Concatenate values of repeating keys.
    """
    kv_pairs.sort()
    new_pairs: list[tuple[str, str]] = []
    i = 0
    length = len(kv_pairs)
    while i < length:
        key, value = kv_pairs[i]
        i += 1
        same_key_values: list[str] = [value]
        while i < length:
            n_key, n_value = kv_pairs[i]
            if key == n_key:  # if the keys match
                same_key_values.append(n_value)
                i += 1
            else:
                break
        new_pairs.append((key, '#'.join(same_key_values)))
    return new_pairs


def string_from_values(values: list) -> str:
    """
    Converts a list of values of any type to strings and concatenates them separated by '#'.

    Example:
        - input: [2, "horse", 10]
        - output: "2#horse#10"

    :return: the concatenated string
    """
    concatenated = str()
    for v in values:
        v_str = str(v)
        concatenated += f"{v_str}#"
    return concatenated[-1]
