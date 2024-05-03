import abc


class ITradingEnvironment(abc.ABC):
    
    @abc.abstractmethod
    def get_price(self, ticker: str) -> float:
        """
        Retrieve the live price of a cryptocurrency asset.

        :param str ticker: A string identifier for the asset.
        """
        pass

    @abc.abstractmethod
    def buy_coin(self, coin_symbol: str, quantity_usd: float) -> bool:
        pass
    
    @abc.abstractmethod
    def sell_coin(self, coin_symbol: str, quantity_coin: float) -> bool:
        pass
    
    @abc.abstractmethod
    def stake_coin(self, pool_id: str, amount0: float, amount1: float) -> bool:
        pass
