"""
    db.py - This module contains the function to connect to the MongoDB database.
"""
import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError

class DB:
    def __init__(self):
        self.client = None
        self.db = None

    def connect(self):
        # Get the MongoDB URI from environment variables
        uri = os.environ.get("MONGODB_URI", "")
        
        if not uri:
            print("MongoDB URI is not set in environment variables")
            exit(1) 

        try:
            self.client = MongoClient(uri)
            self.db = self.client.get_database() 
            print("Connected to MongoDB successfully")
        except PyMongoError as err:
            print("Error connecting to MongoDB:", err)
            exit(1) 