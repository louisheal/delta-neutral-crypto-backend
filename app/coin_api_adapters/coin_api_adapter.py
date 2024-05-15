import abc


class ICoinApiAdapter(abc.ABC):
    
    @abc.abstractmethod
    def get_price(self, ticker: str) -> float:
        """
        Retrieve the live price for a cryptocurrency asset from an API.
        
        :param str ticker: A string identifier for the asset.
        """
        pass
    