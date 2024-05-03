import abc


class IPortfolio(abc.ABC):
    
    @abc.abstractmethod
    def get_quantity_usd(self) -> float:
        pass
    
    @abc.abstractmethod
    def get_quantity_coin(self, coin_symbol: str) -> float:
        pass

    @abc.abstractmethod
    def buy_coin(self, coin_symbol: str, quantity_usd: float, quantity_coin: float) -> bool:
        pass
    
    @abc.abstractmethod
    def sell_coin(self, coin_symbol: str, quantity_usd: float, quantity_coin: float) -> bool:
        pass
    
    @abc.abstractmethod
    def stake_coin(self, pool_id: str, amount0: float, amount1: float) -> bool: 
        pass
    
    @abc.abstractmethod
    def unstake_coin(self, pool_id: str, amount0: float, amount1: float) -> bool:
        pass
    