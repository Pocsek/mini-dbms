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


# def insert_many(db_name: str, collection_name: str, key_value_pairs: list[tuple[str, str]]) -> list[str]:
#     """
#     Insert multiple documents into a collection without any validation.
#     Ordering is not guaranteed.
#     Returns a list of keys of the inserted documents on success.
#     """
#     with pymongo.MongoClient(str(_MongoHost())) as client:
#         db = client[db_name]
#         collection = db[collection_name]
#         documents = [{"_id": key, "value": value} for key, value in key_value_pairs]
#         # noinspection PyUnresolvedReferences
#         try:
#             # insert the documents into mongoDB collection
#             # set ordered=False to continue inserting even if there are duplicate keys
#             result = collection.insert_many(documents, ordered=False)
#         except pymongo.errors.BulkWriteError as e:
#             # catch the error if there are duplicate keys
#             # get the duplicate keys from the error message
#
#             pass
#         return True, []


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

