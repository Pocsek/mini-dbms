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


def get_databases() -> []:
    return dbs['databases']

