import abc

from app.farming_pools.pool import Pool


class IFarmingPlatformApi(abc.ABC):
    
    # TODO: Add docstrings
    @abc.abstractmethod
    def get_pools(self) -> list[Pool]:
        pass
    
    @abc.abstractmethod
    def get_pool_by_id(self, pool_id: str) -> Pool:
        pass
