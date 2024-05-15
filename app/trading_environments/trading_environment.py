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
    def buy_coin(self, coin_symbol: str, quantity_dai: float) -> bool:
        pass
    
    @abc.abstractmethod
    def sell_coin(self, coin_symbol: str, quantity_coin: float) -> bool:
        pass
    
    @abc.abstractmethod
    def stake_coin(self, pair_id: str, quantity_one: float, quantity_two: float) -> bool:
        pass
    
    @abc.abstractmethod
    def unstake_coin(self, pair_id: str, quantity_lp_tokens: float) -> bool:
        pass
