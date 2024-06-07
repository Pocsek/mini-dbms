import json
import os

from server_side.database_objects import Database, Table, Column, Index, PrimaryKey, ForeignKey, mongo_db
from server_side import __working_dir__
from server_side.interpreter import datatypes


class DbManager:
    __dbs: list[Database] = []
    __working_db = 0  # the index of the database we're currently using
    __prev_working_db = 0  # the index of the database we were using on the last stable state
    # the file where the database sceleton is stored:
    __db_file: str = os.path.join(__working_dir__, "databases.json")

    def __init__(self):
        mongo_db.close_down()  # close the MongoDB client if it's open
        mongo_db.set_up()  # start the new MongoDB client
        self.load_databases()

    def __dict__(self) -> dict:
        return {
            "databases": [db.__dict__() for db in self.__dbs],
            "working_db": self.__working_db
        }

    def load_databases(self):
        if os.path.exists(self.__db_file):
            self.__dbs = self.get_previous_state()
        else:
            with open(self.__db_file, "w") as f:
                self.__dbs = self.create_default_databases()
                json.dump([db.__dict__() for db in self.__dbs], f, indent=4)

    def update_db_structure_file(self):
        with open(self.__db_file, "w") as f:
            json.dump([db.__dict__() for db in self.__dbs], f, indent=4)

    def get_previous_state(self) -> list[Database]:
        """
        Loads and returns the previous state of the database structure file.
        """
        if os.path.exists(self.__db_file):
            with open(self.__db_file, "r") as f:
                data: list[dict] = json.load(f)  # decode (JSON -> python dict)
                return [Database().from_dict(db) for db in data]
        raise FileNotFoundError("Database structure file not found.")

    def revert_changes(self):
        prev_dbs: list[Database] = self.get_previous_state()
        # resetting mongo can cause problems that the structure sync can fix, so we do it first
        self.reset_mongo_modifications()
        self.sync_structure_with_mongo(prev_dbs, self.get_databases())
        self.__dbs = prev_dbs
        self.__working_db = self.__prev_working_db
        print("Changes reverted.")

    def save_changes(self):
        """
        Compare the previous state of the structure file with the current state.
        If anything has changed, save the changes to the database too.
        Then update the structure file.
        """
        prev_dbs: list[Database] = self.get_previous_state()  # load the previous state of the structure file
        self.sync_structure_with_mongo(self.get_databases(), prev_dbs)  # sync the structure file with the database
        mongo_db.drop_database("_temp")  # drop the temporary database used for the transaction
        self.update_db_structure_file()  # update the structure file
        self.__prev_working_db = self.__working_db
        print("Changes saved.")

    def reset_mongo_modifications(self):
        """
        Load collections from the _temp database into their original, then drop the _temp database.
        """
        temp_db_name: str = "_temp"
        temp_coll_names: list[str] = mongo_db.get_collection_names(temp_db_name)
        # each collection in the temporary database has a name like: __dbname#tablename
        for temp_coll_name in temp_coll_names:
            db_name, table_name = temp_coll_name[2:].split("#")  # remove the first two characters and split by '#'
            mongo_db.overwrite_collection(temp_db_name, temp_coll_name, db_name, table_name)
        mongo_db.drop_database(temp_db_name)  # drop the temporary database
        print("MongoDB modifications reset.")

    def sync_structure_with_mongo(self, next_dbs: list[Database], prev_dbs: list[Database]):
        """
        Sync two states of the structure file with the database.
        Whatever is in the next state but not in the previous state nor in the database, will be created.
        :param next_dbs: represents the next state of the structure file
        :param prev_dbs: represents the previous state of the structure file
        :return:
        """
        for db in next_dbs:
            self.sync_database_with_mongo(db)
        prev_db_names: list[str] = [db.get_name() for db in prev_dbs]
        next_db_names: list[str] = [db.get_name() for db in next_dbs]
        # drop databases that we don't want in the next state of our database structure
        old_db_names: list[str] = [prev_db for prev_db in prev_db_names if prev_db not in next_db_names]
        for db in old_db_names:
            mongo_db.drop_database(db)

    def sync_database_with_mongo(self, db: Database):
        """
        Create tables and indexes that are in the database object but not in MongoDB.
        Drop tables and indexes that are in MongoDB but not in the database object.
        """
        curr_tables: list[Table] = db.get_tables()
        # table and index collection names in MongoDB:
        mongo_coll_names: list[str] = mongo_db.get_collection_names(db.get_name())
        curr_index_coll_names: list[str] = []
        for table in curr_tables:  # create tables, and it's index collections if they are not present
            if table.get_name() not in mongo_coll_names:
                mongo_db.create_collection(db.get_name(), table.get_name())
            else:
                mongo_coll_names.remove(table.get_name())
            # index collections should be made by this stage, but if not, create them
            for index in table.get_indexes():
                coll_name = _build_collection_name_for_index(table.get_name(), index.get_name())
                curr_index_coll_names.append(coll_name)  # store the index collection names
                if coll_name not in mongo_coll_names:
                    mongo_db.create_collection(db.get_name(), coll_name)
                else:
                    mongo_coll_names.remove(coll_name)

        curr_table_names: list[str] = [table.get_name() for table in curr_tables]
        mongo_coll_names.remove("__next_identity")
        # drop tables and index collections that are in MongoDB but not in the database object
        for coll_name in mongo_coll_names:
            if coll_name not in curr_table_names or coll_name not in curr_index_coll_names:
                mongo_db.drop_collection(db.get_name(), coll_name)

    def create_table(self, table: Table):
        # create collection in MongoDB
        mongo_db.create_collection(self.get_working_db().get_name(), table.get_name())

        # create document in '__next_identity' collection, storing the next identity value of this table
        # (only if it has an identity column)
        identity_col = table.get_identity_column()
        if identity_col:
            seed = identity_col.get_identity_seed()
            identity_collection_name: str = "__next_identity"
            mongo_db.save_collection(self.get_working_db().get_name(), identity_collection_name)
            mongo_db.insert_one_int(self.get_working_db().get_name(),
                                    identity_collection_name,
                                    (table.get_name(), seed))

        # update structure file
        self.get_working_db().add_table(table)
        # self.update_db_structure_file()

    def create_index(self, index: Index, table_name: str):
        table: Table = self.get_table(self.get_working_db_index(), table_name)
        pr_key_names: list[str] = table.get_primary_key().get_column_names()
        column_names: list[str] = table.get_column_names()

        # create a collection with concatenated table name and index name that starts with an '__'
        coll_name: str = _build_collection_name_for_index(table_name, index.get_name())  # collection name
        mongo_db.create_collection(self.get_working_db().get_name(), coll_name)
        selection: dict = {}
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
        mongo_db.save_collection(self.get_working_db().get_name(), coll_name)
        for key_value_pair in idx_kv_pairs:
            try:
                mongo_db.insert_one(self.get_working_db().get_name(), coll_name, key_value_pair)
            except ValueError:
                raise

        # update structure file
        table.add_index(index)
        # self.update_db_structure_file()

    def drop_database(self, db_name):
        # delete db in MongoDB
        mongo_db.drop_database(db_name)

        # update json structure
        self.__dbs.pop(self.get_db_index(db_name))
        # self.update_db_structure_file()

    def drop_table(self, table_name):
        """
        Delete index collections if they exist.
        Delete collection in MongoDB.
        Delete identity value from the __next_identity collection if identity is set.
        """
        for index in self.get_working_db().get_table(table_name).get_indexes():
            coll_name = _build_collection_name_for_index(table_name, index.get_name())
            mongo_db.drop_collection(self.get_working_db().get_name(), coll_name)
        mongo_db.drop_collection(self.get_working_db().get_name(), table_name)

        # delete identity value from the __next_identity collection if identity is set
        identity_col = self.get_table(self.get_working_db_index(), table_name).get_identity_column()
        if identity_col:
            mongo_db.save_collection(self.get_working_db().get_name(), "__next_identity")
            mongo_db.delete(self.get_working_db().get_name(), "__next_identity", {"_id": table_name})

        # update structure, this should be done in the end because the table is needed for other operations
        db = self.get_working_db()
        db.remove_table(table_name)

    def get_default_database_names(self) -> list[str]:
        return ["master"]

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

    def get_index_name(self, db_name, table_name, col_name):
        table: Table = self.get_table(self.get_db_index(db_name), table_name)
        return table.get_index_by_column_names([col_name]).get_name()

    def get_next_identity_value(self, db_name: str, table_name: str) -> int:
        """
        Retrieves the next identity value of a table and increments that value inside the __next_identity collection.
        :return: the next identity value of the given table
        """
        document = mongo_db.select(db_name, "__next_identity", {"_id": table_name})[0]
        next_identity = document.get("value")
        identity_increment = self.get_table(
            self.find_database(db_name),
            table_name
        ).get_identity_column().get_identity_increment()
        mongo_db.increment_identity(db_name, table_name, identity_increment)
        return next_identity

    def add_database(self, db: Database):
        """
        Add new database to the list of databases.

        Create a default collection in the database (this information is only visible inside MongoDB) which stores the
        last identity value of every table with an identity column.
        Each document in the collection contains the table name and its last identity value.
        """
        self.__dbs.append(db)
        mongo_db.create_collection(db.get_name(), "__next_identity")

    def insert(self, db: Database, tb: Table, records: list[dict]) -> list[str]:
        """
        Inserts records into a table creating key-value pairs.
        Inserts records into the index collections if they exist.
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
        key_value_pairs: list[tuple[str, str]] = []
        for record in records:
            key, value = build_key_value_pair(record, column_names, primary_key_names)
            key_value_pairs.append((key, value))
        inserted_keys = []
        indexes: list[Index] = tb.get_indexes()
        mongo_db.save_collection(db.get_name(), tb.get_name())
        for key_value_pair, record in zip(key_value_pairs, records):
            try:
                inserted_keys.append(mongo_db.insert_one(db.get_name(), tb.get_name(), key_value_pair))
                for index in indexes:
                    i_col_names: list[str] = index.get_column_names()
                    # get the values for the index columns and concatenate them
                    coll_keys: list[str] = [record[n] for n in i_col_names]
                    coll_key = string_from_values(coll_keys)  # collection key
                    coll_name = _build_collection_name_for_index(tb.get_name(), index.get_name())
                    mongo_db.save_collection(db.get_name(), coll_name)
                    # get the record from the index collection if it exists
                    result = mongo_db.select(db.get_name(), coll_name, {"_id": coll_key})
                    if tb.is_unique(i_col_names):
                        # if the column names for the index are unique insert the record into the index collection
                        # for insertion use the key part of the inserted record as value
                        # and the collection key generated for the index as key
                        mongo_db.insert_one(db.get_name(), coll_name, (coll_key, key_value_pair[0]))
                    else:
                        # if the column names for the index are not unique update the index collection if the key exists
                        if result:
                            # if the key exists in the index collection update the value
                            new_value: str = string_from_values([result[0].get("value"), key_value_pair[0]])
                            mongo_db.update_one(db.get_name(),
                                                coll_name,
                                                {"_id": coll_key},
                                                {"$set": {"value": new_value}})
                        else:
                            # if the key does not exist in the index collection insert the record
                            mongo_db.insert_one(db.get_name(), coll_name, (coll_key, key_value_pair[0]))

            except ValueError:
                raise
        return inserted_keys

    def delete(self, db: Database, tb: Table, key: str) -> int:
        """
        Deletes records from index collections if they exist.
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
        results = mongo_db.select(db.get_name(), tb.get_name(), {"_id": key})
        if len(results) == 0:
            return 0
        result = results[0]
        record: dict = split_key_value_pair(result, tb.get_column_names(), tb.get_primary_key().get_column_names())
        indexes = tb.get_indexes()
        for index in indexes:
            i_col_names: list[str] = index.get_column_names()
            coll_name = _build_collection_name_for_index(tb.get_name(), index.get_name())
            mongo_db.save_collection(db.get_name(), coll_name)
            if tb.is_unique(i_col_names):
                coll_key = string_from_values([record.get(n) for n in i_col_names])
                mongo_db.delete(db.get_name(), coll_name, {"_id": coll_key})
            else:
                coll_key = string_from_values([record.get(n) for n in i_col_names])
                index_result = mongo_db.select(db.get_name(), coll_name, {"_id": coll_key})
                if index_result[0].get("value") == key:
                    mongo_db.delete(db.get_name(), coll_name, {"_id": coll_key})
                else:
                    values = values_from_string(index_result[0].get("value"))
                    values.remove(key)
                    new_value = string_from_values(values)
                    mongo_db.update_one(db.get_name(), coll_name, {"_id": coll_key}, {"$set": {"value": new_value}})
        mongo_db.save_collection(db.get_name(), tb.get_name())
        del_count = mongo_db.delete(db.get_name(), tb.get_name(), {"_id": key})
        return del_count

    def find_by_primary_key(self, db_name: str, table_name: str, pk_column_values: list) -> str | None:
        """
        Find a record in a table by its primary key.
        The columns need to be part of the primary key.

        Separator character between (attribute) values inside a record is '#'.

        Parameters are not validated here.

        :return: a string consisting of the values corresponding to the primary key if the given key exists, else None
        """
        key = string_from_values(pk_column_values)  # concatenate the column values
        values = mongo_db.select(db_name, table_name, {"_id": key})
        return values[0] if values else None

    def find_by_value(self,
                      db_name: str,
                      table_name: str,
                      column_names: list[str],
                      column_values: list) -> str | None:
        """
        Find the primary key that the given value belong to in a table.
        If the given value is a non-unique value, then find all primary keys that belong to the given value.
        The columns need to be part of the same unique key.

        Separator character between column values inside a primary key is '#'.
        Separator character between primary keys is also '#' (no difference).

        :return: a string: the primary key corresponding to the given value(s) if they exist, else None
        """
        value = string_from_values(column_values)  # column values concatenated into a '#' separated string
        table = self.get_table(self.find_database(db_name), table_name)
        index = table.get_index_by_column_names(column_names)
        if index:
            # for both single and compound values only if there is an index created on all columns, use those to search
            index_collection_name = _build_collection_name_for_index(table_name, index.get_name())
            for kv in mongo_db.select(db_name, index_collection_name):
                if kv.get("_id") == value:
                    return kv.get("value")
        else:
            # get the column positions (a.k.a. indexes) in the table's column list
            col_pos = table.get_column_positions(column_names)

            # iterate through the collection (table)
            for kv in mongo_db.select(db_name, table_name):
                kv_list = kv.get("_id").split("#") + kv.get("value").split("#")
                found = True
                for i in range(len(column_values)):
                    if column_values[i] != kv_list[col_pos[i]]:
                        found = False
                        break
                if found:
                    return kv.get("_id")
        return None



    def find_conditional_indexed_by_primary_key(self,
                                                db_name: str,
                                                table_name: str,
                                                logical_op: str,
                                                condition_value) -> list:
        """
        Find those primary keys and values that fulfill the condition USING the built-in INDEXES.

        ! Currently, condition is always evaluated in the order: <column> <op> <value>

        :param column_name: the column to compare
        :param column_type: the datatype of the column
        :param logical_op: the logical operator used for comparing
        :param condition_value: the value the column is being compared with
        :return: a list of records that fulfill the condition
        """
        mongo_op = self.__logical_op_to_mongo_op(logical_op)
        selection = {"_id": {mongo_op: condition_value}}
        values = mongo_db.select(db_name, table_name, selection)
        return values

    def find_conditional_indexed_by_value(self,
                                          db_name: str,
                                          table_name: str,
                                          column_name: str,
                                          column_type: str,
                                          logical_op: str,
                                          condition_value) -> list:
        """
        Find those values that fulfill the condition USING INDEXES.

        ! Currently, condition is always evaluated in the order: <column> <op> <value>

        :param column_name: the column to compare
        :param column_type: the datatype of the column
        :param logical_op: the logical operator used for comparing
        :param condition_value: the value the column is being compared with
        :return: a list of primary keys (not in concatenated format) of records that fulfill the condition
        """
        result = []
        table = self.get_table(self.find_database(db_name), table_name)
        pk_length = len(table.get_primary_key().get_column_names())
        index = table.get_index_by_column_names([column_name])
        index_collection_name = _build_collection_name_for_index(table_name, index.get_name())
        for kv in mongo_db.select(db_name, index_collection_name):
            k = kv.get("_id").split("#")[0]  # [0] for now
            k = datatypes.cast_value(k, column_type)
            fulfills = datatypes.eval_logical_expression(k, logical_op, condition_value)
            if not fulfills:
                continue
            v = kv.get("value").split("#")
            for i in range(0, len(v), pk_length):
                # take out length of primary key number of elements from the list with values to get one primary key
                result.append(v[i:i + pk_length])
        return result

    def __logical_op_to_mongo_op(self, op: str):
        match op:
            case "<":
                return "$lt"
            case ">":
                return "$gt"
            case "<=":
                return "$lte"
            case ">=":
                return "$gte"
            case "=":
                return "$eq"
            case _:
                raise NotImplementedError(f"Invalid operator'{op}'")

    def find_all(self, db_name: str, table_name: str) -> list[list]:
        """
        Find all records in a table.

        :return: a list of records where a record is a list of values
        """
        result = []
        for kv in mongo_db.select(db_name, table_name):
            k = kv.get("_id").split("#")
            v = kv.get("value").split("#")
            if v[-1] == "":
                v = v[:-1]
            kv_list = k + v
            result.append(kv_list)
        return result

    def query_index_collection(self, db_name, table_name, col_name, op, cond_val: str) -> list[tuple] | None:
        """
        :return:
        """
        idx_name = self.get_index_name(db_name, table_name, col_name)
        collection_name = _build_collection_name_for_index(table_name, idx_name)
        mongo_op = self.__logical_op_to_mongo_op(op)
        selection = {"_id": {mongo_op: str(cond_val)}}
        kv_pairs: list[dict] = mongo_db.select(db_name, collection_name, selection)
        if len(kv_pairs) == 0:
            return None
        result: list[tuple] = []
        for kv_p in kv_pairs:
            key = kv_p.get("_id")
            val = kv_p.get("value")
            if "#" in key:
                raise NotImplementedError("Composite indexes are not supported")
            result.append((key, val.split('#')))
        return result

    def create_default_databases(self) -> list[Database]:
        dbs: list[Database] = []
        for name in self.get_default_database_names():
            db = Database(name=name)
            dbs.append(db)
            mongo_db.create_collection(db.get_name(), "__next_identity")
        return dbs

    def join_tables(self, db_idx: int, tb_1: Table, tb_2: Table, op: str, col_name_1: str, col_name_2: str) ->list[list]:
        """ """
        if op != "=":
            raise NotImplementedError(f"Join operation '{op}' not implemented")
        outer = tb_1.get_name()
        outer_col = col_name_1
        outer_idx = tb_1.find_column(col_name_1)
        inner = tb_2.get_name()
        inner_col = col_name_2
        inner_idx = tb_2.find_column(col_name_2)

        if not tb_1.column_is_indexed(col_name_1) and not tb_2.column_is_indexed(col_name_2):
            # nested loop join
            outer_records: list[list] = self.find_all(self.get_databases()[db_idx].get_name(), outer)
            inner_records: list[list] = self.find_all(self.get_databases()[db_idx].get_name(), inner)
            result: list[list] = []
            for o_rec in outer_records:
                for i_rec in inner_records:
                    if o_rec[outer_idx] == i_rec[inner_idx]:  # join condition is met (only '=' works)
                        result.append(o_rec + i_rec)
            return result
        swap: bool = False
        if tb_1.column_is_indexed(col_name_1) and not tb_2.column_is_indexed(col_name_2):
            # swap them so that the indexed one is the inner table
            outer, inner = inner, outer
            outer_col, inner_col = inner_col, outer_col
            swap = True
            outer_records: list[list] = self.find_all(self.get_databases()[db_idx].get_name(), outer)
            for o_rec in outer_records:
                raise NotImplementedError("Join operation not implemented for indexed columns")
                i_key = o_rec[outer_idx]
                i_rec = self.find_by_value(self.get_databases()[db_idx].get_name(), inner, inner_col, i_key)
                if i_rec:
                    result.append(o_rec + i_rec)




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
    return '#'.join([str(v) for v in values])


def values_from_string(concatenated: str) -> list:
    """
    Converts a concatenated string of values separated by '#' to a list of values.

        Example:
        - input: "2#horse#10"
        - output: [2, "horse", 10]

    :return: the list of values
    """
    return concatenated.split("#")


def _build_collection_name_for_index(table_name: str, index_name: str):
    """
    Concatenate table name and index name with some special characters to create a collection name for the index.
    """
    return "__" + table_name + '#' + index_name
