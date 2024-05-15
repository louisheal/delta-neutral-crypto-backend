import abc


class ICoinApi(abc.ABC):
    
    @abc.abstractmethod
    def get_price_by_symbol(self, symbol: str) -> float:
        """
        Retrieve the live price for a cryptocurrency asset from an API.
        
        :param str symbol: A string identifier for the asset.
        """
        pass
    