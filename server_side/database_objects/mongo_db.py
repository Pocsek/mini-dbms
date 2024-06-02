import pymongo

# MongoDB client, no outside access is allowed.
__client__: pymongo.MongoClient | None = None


def set_mongo_host(host_str: str | None = None):
    """
    Set the MongoDB host string.
    """
    global __client__
    if __client__ is not None:
        raise ConnectionError("MongoDB client is already connected. Close the client first.")
    if host_str is None:
        host_str = "mongodb://localhost:27017"
    __client__ = pymongo.MongoClient(host_str)


def close_mongo_client():
    """
    Close the MongoDB client.
    """
    global __client__
    if __client__ is not None:
        __client__.close()
        __client__ = None


def insert_one(db_name: str, collection_name: str, key_value_pair: tuple[str, str]) -> str:
    """
    Insert a document into a collection without any validation.
    Returns the key of the inserted document on success.
    """
    global __client__
    db = __client__[db_name]
    collection = db[collection_name]
    # noinspection PyUnresolvedReferences
    try:
        key, value = key_value_pair
        collection.insert_one({"_id": key, "value": value})  # insert a key-value pair into mongoDB collection
    except pymongo.errors.DuplicateKeyError:
        # catch the error if there are duplicate keys
        raise ValueError(f"Duplicate key [{key}] in collection [{collection_name}]")
    return key


def insert_one_int(db_name: str, collection_name: str, key_value_pair: tuple[str, int]) -> str:
    """
    Insert a document into a collection with the value part as an integer.
    """
    global __client__
    db = __client__[db_name]
    collection = db[collection_name]
    key, value = key_value_pair
    collection.insert_one({"_id": key, "value": value})  # insert a key-value pair into mongoDB collection
    return key


def create_collection(db_name: str, collection_name: str):
    """
    Create new collection in a database.
    """
    global __client__
    db = __client__[db_name]
    db.create_collection(collection_name)


def drop_database(db_name: str):
    """
    Deletes a database only if it exists.
    """
    global __client__
    if db_name in __client__.list_database_names():
        __client__.drop_database(db_name)


def drop_collection(db_name: str, collection_name: str):
    """
    Deletes a collection.
    """
    global __client__
    db = __client__[db_name]
    db.drop_collection(collection_name)


def delete(db_name: str, collection_name: str, query: dict) -> int:
    """
    Deletes documents from a collection, without any validation.
    Returns the number of deleted documents.
    """
    global __client__
    db = __client__[db_name]
    collection = db[collection_name]
    result = collection.delete_many(query)
    return result.deleted_count


def get_database_names() -> list[str]:
    """
    Get a list of database names.
    """
    global __client__
    return __client__.list_database_names()


def get_collection_names(db_name: str) -> list[str]:
    """
    Get a list of collection names in a database.
    """
    global __client__
    db = __client__[db_name]
    return db.list_collection_names()


def select(db_name: str, collection_name: str, selection: dict = None) -> list[dict]:
    """
    Sends the query to the database and returns a key-value based dictionary.
    :param db_name: name of the database
    :param collection_name: name of the collection
    :param selection: query to filter the documents
    """
    global __client__
    db = __client__[db_name]
    collection: pymongo.collection.Collection = db[collection_name]
    result = collection.find(selection if not None else {}, {"_id": 1, "value": 1})
    return list(result)


def increment_identity(db_name: str, table_name: str, increment_by: int):
    """
    Increment the next identity value of a table in the __next_identity collection of the given database.
    """
    global __client__
    db = __client__[db_name]
    collection_name = "__next_identity"
    collection: pymongo.collection.Collection = db[collection_name]
    filter_criteria = {"_id": table_name}
    update_operation = {"$inc": {"value": increment_by}}
    result = collection.update_one(filter_criteria, update_operation)
    if result.matched_count == 0:
        raise ValueError(
            f"Failed to increment next identity value in collection [{collection_name}] for table [{table_name}]."
        )


def update_one(db_name: str, collection_name: str, query: dict, update: dict):
    """
    Update a document in a collection.
    No validation is performed.
    """
    global __client__
    db = __client__[db_name]
    collection = db[collection_name]
    collection.update_one(query, update)
