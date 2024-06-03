from unittest import TestCase

from server_side.database_objects import mongo_db


class TestMongoDB(TestCase):
    """
    Test the MongoDB functions.
    """

    def setUp(self) -> None:
        """
        Set up the test.
        """
        mongo_db.close_down()
        mongo_db.set_up()

    def test_insert_one(self):
        """
        Test the insert_one function.
        """
        try:
            mongo_db.drop_database("test_db")
            key = mongo_db.insert_one("test_db", "test_collection", ("key", "value"))
            print(key)

        finally:
            pass

    def test_insert_one_int(self):
        """
        Test the insert_one_int function.
        """
        try:
            mongo_db.drop_database("test_db")
            key = mongo_db.insert_one_int("test_db", "test_collection", ("key", 1))
            print(key)

        finally:
            pass

    def test_create_collection(self):
        """
        Test the create_collection function.
        """
        try:
            mongo_db.drop_database("test_db")
            r = mongo_db.create_collection("test_db", "test_collection")
            print(r)

        finally:
            pass

    def test_drop_collection(self):
        """
        Test the drop_collection function.
        """
        try:
            mongo_db.drop_database("test_db")
            mongo_db.create_collection("test_db", "test_collection1")
            mongo_db.create_collection("test_db", "test_collection2")

            r = mongo_db.drop_collection("test_db", "test_collection1")
            print(r)

        finally:
            pass




