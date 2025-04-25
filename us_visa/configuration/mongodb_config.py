import pymongo
from us_visa.logger import logging
from us_visa.exception import USVISAEXCEPTION
import os
from dotenv import load_dotenv
import sys
load_dotenv()




class DB_CONNECTION:
    def __init__(self,db,collection):
        self.db = db
        self.collection = collection
        self.mongo_connection = "mongodb+srv://prashantsinghaiengineer:6lT4EGmuVUwxPkMU@cluster0.q3083.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    def load_data(self):
        try:
            if self.mongo_connection:
                logging.info("MongoDB connection is establish")
                client = pymongo.MongoClient(self.mongo_connection)
                Mongo_db = client[self.db]
                Mongo_collection = Mongo_db[self.collection]
                return Mongo_collection
            else:
                logging.info("Mongo db connection is not establish")
        except Exception as e:
            logging.info(f"{USVISAEXCEPTION(e,sys) }")
