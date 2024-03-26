import json
import os


class IndexManager:
    def __init__(self):
        self.indexes: dict = dict()
        self.file: str = "indexes.json"
        if not os.path.exists(self.file):
            # create index structure if it doesn't already exist
            with open(self.file, "w") as f:
                structure: dict = {"indexes": [dict()]}
                json.dump(structure, f, indent=2)

    def load_indexes(self):
        # load JSON file into self.indexes
        with open(self.file, "r") as f:
            self.indexes = json.load(f)

    def update_indexes(self):
        # overwrite JSON file with current state of self.indexes
        with open(self.file, "w") as f:
            json.dump(self.indexes, f, indent=2)


def create_empty_index() -> dict:
    return {
        "name": "",
        "database": "",
        "table": "",
        "columns": [],
        "index": ""
    }
