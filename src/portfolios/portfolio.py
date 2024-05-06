import abc


class IPortfolio(abc.ABC):
    
    @abc.abstractmethod
    def get_quantity_dai(self) -> float:
        pass
    
    @abc.abstractmethod
    def get_quantity_coin(self, coin_symbol: str) -> float:
        pass

    @abc.abstractmethod
    def buy_coin(self, coin_symbol: str, quantity_dai: float, quantity_coin: float) -> bool:
        pass
    
    @abc.abstractmethod
    def sell_coin(self, coin_symbol: str, quantity_dai: float, quantity_coin: float) -> bool:
        pass
    
    @abc.abstractmethod
    def stake_coin(self, pool_id: str, symbol_one: float, symbol_two: float, quantity_one: float, quantity_two: float, quantity_lp_tokens: float) -> bool: 
        pass
    
    @abc.abstractmethod
    def unstake_coin(self, pool_id: str, symbol_one: float, symbol_two: float, quantity_one: float, quantity_two: float, quantity_lp_tokens: float) -> bool: 
        pass
    