import abc


class IPortfolio(abc.ABC):
    
    def get_quantity_usd(self) -> float:
        pass
    
    def get_quantity_coin(self, coin_symbol: str) -> float:
        pass

    def buy_coin(self, coin_symbol: str, quantity_usd: float, quantity_coin: float) -> bool:
        pass
    
    def sell_coin(self, coin_symbol: str, quantity_usd: float, quantity_coin: float) -> bool:
        pass
    