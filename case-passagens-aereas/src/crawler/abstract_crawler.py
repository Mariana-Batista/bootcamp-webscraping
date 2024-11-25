from abc import ABC, abstractmethod

from src.tools.redis import RedisClient

class AbstractCrawler(ABC):
    
    def __init__(self):
        self.redis = RedisClient.get()
    
    @abstractmethod
    def execute_main(self):
        pass
    
    @abstractmethod
    def execute_before(self):
        pass

    @abstractmethod
    def execute_after(self):
        pass
    
    def get_step(self, key):
        
        steps = None
        
        try:
            steps = self.redis.get(key)
        except:
            print("Falha ao recuperar etapa do Redis.")
        return steps
    
    def save_data(self, data):
        try:
            self.mongo.save_dataframes(data)
        except:
            print("Falha ao salvar dados no MongoDB.")