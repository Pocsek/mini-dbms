import json
import os

dbs = {}  # the databases metadata is loaded into this dictionary
working_db = 0  # the index of the database we're currently using


def load_databases():
    if os.path.exists("databases.json"):
        with open("databases.json", "r") as f:
            data = json.load(f)  # decode (JSON -> python dict)
    else:
        with open("databases.json", "w") as f:
            data = create_default_databases()
            json.dump(data, f, indent=2)
    return data


def update_databases():
    with open("databases.json", "w") as f:
        json.dump(dbs, f, indent=2)  # encode (python dict -> JSON)
        # f.truncate()  # if the new file is smaller, cut off excess space


def get_database(idx):
    if idx >= len(get_databases()):
        raise "Cannot retrieve database: index out of bounds"
    return dbs["databases"][idx]


def get_databases() -> []:
    return dbs["databases"]


def find_database(name) -> int:
    for (idx, db) in enumerate(get_databases()):
        if db["name"] == name:
            return idx
    return -1


def find_table(db_idx, table_name) -> int:
    for (idx, table) in enumerate(dbs["databases"][db_idx]["tables"]):
        if table["table_name"] == table_name:
            return idx
    return -1


def get_table_names(db_idx) -> list[str]:
    table_names = []
    for table in dbs["databases"][db_idx]["tables"]:
        table_names.append(table["table_name"])
    return table_names


def get_column_names(db_idx, table_idx) -> list[str]:
    column_names = []
    for column in dbs["databases"][db_idx]["tables"][table_idx]["columns"]:
        column_names.append(column["name"])
    return column_names


def create_default_databases() -> dict:
    data = {
        "databases": []
    }
    default_db_1 = create_empty_database()
    default_db_1["name"] = "master"
    data["databases"].append(default_db_1)
    return data


def create_empty_database() -> dict:
    return {
        "name": "",
        "tables": []
    }


def create_empty_foreign_key() -> dict:
    return {
        "attributes": [],
        "references": {
            "table": "",
            "attributes": []
        }
    }


def create_empty_table() -> dict:
    return {
        "table_name": "",
        "file_name": "",
        "columns": [],
        "keys": {
            "primary_key": [],
            "foreign_keys": [],
            "unique_keys": []
        },
        "constraints": {
            "check": [],
            "default": []
        },
        "indexes": []
    }


def create_empty_column() -> dict:
    return {
        "name": "",
        "type": "",
        "allow_nulls": True,
        "identity": False,
        "identity_seed": 0,
        "identity_increment": 0
    }


def create_empty_index() -> dict:
    return {
        "name": "",
        "columns": [],
        "index": ""
    }
