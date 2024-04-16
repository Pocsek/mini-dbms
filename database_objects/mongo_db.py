import pymongo


class _MongoHost:
    """
    A class to represent the MongoDB host as a string.
    This class is not meant to be used directly.
    """

    def __init__(self, host_str: str = "mongodb://localhost:27017"):
        self.__host_str: str = host_str

    def __str__(self) -> str:
        return self.__host_str


# TO-DO: error handling
def insert_one(db_name: str, collection_name: str, document: dict) -> bool:
    """
    Insert a document into a collection without any validation.
    """
    with pymongo.MongoClient(str(_MongoHost())) as client:
        db = client[db_name]
        collection = db[collection_name]
        # noinspection PyUnresolvedReferences
        try:
            collection.insert_one(document)  # insert the document into mongoDB collection
        except pymongo.errors.DuplicateKeyError:
            # catch the error if there are duplicate keys
            return False
        return True


def insert_many(db_name: str, collection_name: str, documents: list[dict]) -> bool:
    """
    Insert multiple documents into a collection without any validation.
    """
    with pymongo.MongoClient(str(_MongoHost())) as client:
        db = client[db_name]
        collection = db[collection_name]
        # noinspection PyUnresolvedReferences
        try:
            collection.insert_many(documents)  # insert the documents into mongoDB collection
        except pymongo.errors.BulkWriteError:
            # catch the error if there are duplicate keys
            return False
        return True
