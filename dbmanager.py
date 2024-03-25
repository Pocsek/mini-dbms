import json

dbs = {}  # the databases metadata is loaded into this dictionary
working_db = 0  # the index of the database we're currently using


def load_databases():
    with open("databases.json", "r") as f:
        data = json.load(f)  # decode (JSON -> python dict)
    return data


def update_databases():
    with open("databases.json", "w") as f:
        json.dump(dbs, f, indent=2)  # encode (python dict -> JSON)
        # f.truncate()  # if the new file is smaller, cut off excess space


def get_database(idx):
    if idx >= len(get_databases()):
        raise "Cannot retrive database: index out of bounds"
    return dbs["databases"][idx]


def get_databases() -> []:
    return dbs["databases"]


def find_database(name) -> int:
    for (idx, db) in enumerate(get_databases()):
        if db["name"] == name:
            return idx
    return -1


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