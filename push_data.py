from dotenv import load_dotenv
import sys
import json
import pymongo
load_dotenv('.env')
import os
mongodb_url = os.getenv('MONGO_DB_URL')
print(mongodb_url)

import certifi
cm=certifi.where()

from networksecurity.logging.logger import logging
from networksecurity.exceptions.exception import NetworkSecurityException

import pandas as pd
import numpy as np

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def csv_to_json_converter(self, filepath):
        try:
            data = pd.read_csv(filepath)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def insert_to_mongodb(self, record, database, collection):
        try:
            self.record = record
            self.collection = collection
            self.database = database
            
            self.client = pymongo.MongoClient(mongodb_url)
            self.database = self.client[self.database]
            
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.record)
            return len(self.record)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

if __name__ == '__main__':
    file_path = 'Network_Data/phisingData.csv'
    database = 'MomenAI'
    collection = 'PhishingData'
    
    extractor = NetworkDataExtract()
    records = extractor.csv_to_json_converter(filepath=file_path)
    #print(records)
    no_inserted_count = extractor.insert_to_mongodb(records, database, collection)
    print(no_inserted_count)
