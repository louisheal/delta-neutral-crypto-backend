import abc


class ITradingEnvironment(abc.ABC):
    
    @abc.abstractmethod
    def get_price(self, ticker: str) -> float:
        """
        Retrieve the live price of a cryptocurrency asset.

        :param str ticker: A string identifier for the asset.
        """
        pass
