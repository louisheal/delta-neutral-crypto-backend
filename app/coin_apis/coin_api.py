import abc


class ICoinApi(abc.ABC):
    
    @abc.abstractmethod
    def get_price_by_symbol(self, symbol: str) -> float:
        """
        Retrieves the live price of a cryptocurrency asset from an API.
        
        :param str symbol: A string identifier for the cryptocurrency asset.
        """
        pass
    