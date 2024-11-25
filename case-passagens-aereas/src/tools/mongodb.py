import os
import pandas as pd
from pymongo import MongoClient

class MongoConnection:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance._client = None
            cls._instance._db = None
            cls._instance._collections = None
        return cls._instance
    
    def __init__(self, host='localhost', port=27017, database='teste', collections='data'):
        if self._client is None:
            self.host = os.getenv("MONGO_HOST", host)
            self.port = os.getenv("MONGO_PORT", port)
            self.database_name = os.getenv("MONGO_DATABASE", database)
            self.collections = os.getenv("MONGO_COLLECTIONS", collections)
            self._connect()
            
    def _connect(self):
        self._client = MongoClient(f"mongodb://{self.host}:{self.port}")
        self._db = self._client[self.database_name]
        self._collections = self._db[self.collections]
        
    def save_dataframe(self, df):
        data = df.to_dict(orient = 'records')
        try:
            self._collections.insert_many(data)
        except:
            print("Erro ao salvar dados no MongoDB.")
    
    def close_connection(self):
        if self._client:
            self._client.close()
            print("Conexão encerrada!")