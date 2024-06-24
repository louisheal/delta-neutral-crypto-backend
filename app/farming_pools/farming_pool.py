import abc

from app.farming_pools.pool import Pool


class IFarmingPool(abc.ABC):
    
    @abc.abstractmethod
    def get_pools(self) -> list[Pool]:
        """
        Retrieves all the available farming pools from a leveraged yield farming platform.
        """
        pass
    
    @abc.abstractmethod
    def get_pool_by_id(self, pool_id: str) -> Pool:
        """
        Retrieves the farming pool with the id `pool_id` from a leveraged yield farming platform.

        :param str pool_id: A string identifier for the farming pool.
        """
        pass
