from abc import ABC, abstractmethod

from src.tools.redis import RedisClient

class AbstractCrawler(ABC):
    
    def __init__(self):
        self.redis = RedisClient.gewt()
    
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
        return self.redis.get(key)
    
    def save_data(self):
        pass