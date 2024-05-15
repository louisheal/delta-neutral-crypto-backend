import abc

class IFarmingPool(abc.ABC):
    
    @abc.abstractmethod
    def get_pools(self):
        pass
