import abc


class ITradingEnvironment(abc.ABC):
    
    @abc.abstractmethod
    def get_price(self, symbol: str) -> float:
        """
        Retrieve the live price of a cryptocurrency asset.

        :param str symbol: A string identifier for the asset.
        """
        pass
