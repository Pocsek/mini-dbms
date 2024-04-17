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


def insert_one(db_name: str, collection_name: str, key: str, value: str) -> bool:
    """
    Insert a document into a collection without any validation.
    Returns True if the document is inserted successfully.
    Returns False if there are duplicate keys.
    """
    with pymongo.MongoClient(str(_MongoHost())) as client:
        db = client[db_name]
        collection = db[collection_name]
        # noinspection PyUnresolvedReferences
        try:
            collection.insert_one({"_id": key, "value": value})  # insert a key-value pair into mongoDB collection
        except pymongo.errors.DuplicateKeyError:
            # catch the error if there are duplicate keys
            return False
        return True


def insert_many(db_name: str, collection_name: str, documents: list[dict]) -> tuple[bool, list]:
    """
    Insert multiple documents into a collection without any validation.
    Ordering is not guaranteed.
    If there are duplicate keys, the function will return False and a list of duplicate keys.
    Otherwise, the function will return True and an empty list.
    """
    with pymongo.MongoClient(str(_MongoHost())) as client:
        db = client[db_name]
        collection = db[collection_name]
        # noinspection PyUnresolvedReferences
        try:
            # insert the documents into mongoDB collection
            # set ordered=False to continue inserting even if there are duplicate keys
            collection.insert_many(documents, ordered=False)
        except pymongo.errors.BulkWriteError as e:
            # catch the error if there are duplicate keys
            # return the list of duplicate keys
            return False, [error["op"]["_id"] for error in e.details["writeErrors"]]
        return True, []


def delete_one(db_name: str, collection_name: str, query: dict) -> bool:
    """
    Delete a document from a collection, without any validation.
    Returns True if the document is deleted successfully.
    Returns False if the document is not found.
    """
    with pymongo.MongoClient(str(_MongoHost())) as client:
        db = client[db_name]
        collection = db[collection_name]
        result = collection.delete_one(query)
        return result.deleted_count > 0


# TO-DO: implement delete_many
def delete_many():
    pass


# # not very useful cause mongoDB doesn't create the database until a collection is created
# def create_database(name: str) -> bool:
#     """
#     Create a new database.
#     Returns True if the database is created successfully.
#     Returns False if the database already exists.
#     """
#     with pymongo.MongoClient(str(_MongoHost())) as client:
#         db_list = client.list_database_names()
#         if name in db_list:
#             print(name)
#             return False
#         _ = client[name]
#         return True


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

