from ..coin_api_adapters.coin_api_adapter import ICoinApiAdapter
from .trading_environment import ITradingEnvironment


class SimulatedTradingEnvironment(ITradingEnvironment):
    
    def __init__(self, coin_api: ICoinApiAdapter):
        self.coin_api = coin_api
    
    def get_price(self, symbol: str) -> float:
        return self.coin_api.get_price(symbol)
