import certifi
import configparser
from http import server
from fastapi import APIRouter, Request
from pymongo import MongoClient

config = configparser.ConfigParser()
config.read(f'app/common/config.ini')

ca = certifi.where()

class MONGO:
    def __init__(self) -> None:
        self.username = config['MONGO']['username']
        self.password = config['MONGO']['password']
        self.database = config['MONGO']['database']
        self.client   = MongoClient(f'mongodb+srv://{self.username}:{self.password}@dev.9symjuu.mongodb.net/', tlsCAFile=ca)
        self.db       = self.client[f'{self.database}']

    def select(self, collection, data):
        result = {}
        try:
            result = self.db[f'{collection}'].find_one(data)
        except Exception as e:
            print(e)
        return result
            
    # def select(self, collection, data):
    #     try:
    #         print(self.db[f'{collection}'])
    #         self.db[f'{collection}'].find(data)
    #     except Exception as e:
    #         print(e)            

    def insert_one(self, collection, data):
        try:
            self.db[f'{collection}'].insert_one(data)
        except Exception as e:
            print(e)

    def insert_many(self, collection, data):
        try:
            self.db[f'{collection}'].insert_many(data)
        except Exception as e:
            print(e)

    def update_one(self, collection, data):
        try:
            self.db[f'{collection}'].update_one(data)
        except Exception as e:
            print(e)

    def update_many(self, collection, data):
        try:
            self.db[f'{collection}'].update_many(data)
        except Exception as e:
            print(e)

