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


def insert_one(db_name: str, collection_name: str, key_value_pair: tuple[str, str]) -> str:
    """
    Insert a document into a collection without any validation.
    Returns the key of the inserted document on success.
    """
    with pymongo.MongoClient(str(_MongoHost())) as client:
        db = client[db_name]
        collection = db[collection_name]
        # noinspection PyUnresolvedReferences
        try:
            key, value = key_value_pair
            collection.insert_one({"_id": key, "value": value})  # insert a key-value pair into mongoDB collection
        except pymongo.errors.DuplicateKeyError:
            # catch the error if there are duplicate keys
            raise ValueError(f"Duplicate key [{key}] in collection [{collection_name}]")
        return key


def create_collection(db_name: str, collection_name: str):
    """
    Create new collection in a database.
    """
    with pymongo.MongoClient(str(_MongoHost())) as client:
        db = client[db_name]
        db.create_collection(collection_name)


def drop_database(db_name: str):
    """
    Deletes a database only if it exists.
    """
    with pymongo.MongoClient(str(_MongoHost())) as client:
        if db_name in client.list_database_names():
            client.drop_database(db_name)


def drop_collection(db_name: str, collection_name: str):
    """
    Deletes a collection.
    """
    with pymongo.MongoClient(str(_MongoHost())) as client:
        db = client[db_name]
        db.drop_collection(collection_name)


def delete(db_name: str, collection_name: str, query: dict) -> int:
    """
    Deletes documents from a collection, without any validation.
    Returns the number of deleted documents.
    """
    with pymongo.MongoClient(str(_MongoHost())) as client:
        db = client[db_name]
        collection = db[collection_name]
        result = collection.delete_many(query)
        return result.deleted_count


def get_database_names() -> list[str]:
    """
    Get a list of database names.
    """
    with pymongo.MongoClient(str(_MongoHost())) as client:
        return client.list_database_names()


def get_collection_names(db_name: str) -> list[str]:
    """
    Get a list of collection names in a database.
    """
    with pymongo.MongoClient(str(_MongoHost())) as client:
        db = client[db_name]
        return db.list_collection_names()


def select(db_name: str, collection_name: str, selection: dict = None) -> list[dict]:
    """
    Sends the query to the database and returns the key-value pairs.
    :param db_name: name of the database
    :param collection_name: name of the collection
    :param selection: query to filter the documents
    """
    with pymongo.MongoClient(str(_MongoHost())) as client:
        db = client[db_name]
        collection: pymongo.collection.Collection = db[collection_name]
        result = collection.find(selection if not None else {}, {"_id": 1, "value": 1})
        return list(result)

