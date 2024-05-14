import abc

class IFarmingPlatform(abc.ABC):
    
    @abc.abstractmethod
    def get_pools(self):
        pass
