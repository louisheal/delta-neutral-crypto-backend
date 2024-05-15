import abc

from .pair import Pair


class ILiquidityPoolApi(abc.ABC):
    
    @abc.abstractmethod
    def get_pair(self, pair_id: str) -> Pair:
        pass
