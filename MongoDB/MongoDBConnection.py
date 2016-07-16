from pymongo import MongoClient


class MongoDBConnection:

    def __init__(self):
        self.client = MongoClient("mongodb://localhost")

    # Returns the MongoDB Connection
    def get_con(self):
        return self.client

    # Returns database by name
    def get_db_by_name(self, name):
        db = self.client[name]
        return db

    # Returns Collection by database and name
    def get_coll_by_db_and_name(self, db, name):
        return self.client[db][name]

    # Sets object with id by database and name
    def set_to_db_and_coll_with_id(self, id, data, db, name):
        data['_id'] = id
        print data['_id']
        self.client[db][name].insert_one(data)

    # Inserts object in collection by database and name
    def set_to_db_and_coll(self, data, db, name):
        self.client[db][name].insert_one(data)