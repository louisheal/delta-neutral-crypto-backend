from ..coin_api_adapters.coin_api_adapter import ICoinApiAdapter
from .trading_environment import ITradingEnvironment
from ..portfolios.portfolio import IPortfolio


class SimulatedTradingEnvironment(ITradingEnvironment):
    
    def __init__(self, coin_api: ICoinApiAdapter, portfolio: IPortfolio):
        self.coin_api = coin_api
        self.portfolio = portfolio
    
    def get_price(self, coin_symbol: str) -> float:
        return self.coin_api.get_price(coin_symbol)
    
    def buy_coin(self, coin_symbol: str, quantity_usd: float) -> bool:

        if self.portfolio.get_quantity_usd() < quantity_usd:
            return False
        
        quantity_coin = quantity_usd / self.get_price(coin_symbol)
        return self.portfolio.buy_coin(coin_symbol, quantity_usd, quantity_coin)
    
    def sell_coin(self, coin_symbol: str, quantity_coin: float) -> bool:
        
        if self.portfolio.get_quantity_coin(coin_symbol) < quantity_coin:
            return False

        quantity_usd = quantity_coin * self.get_price(coin_symbol)
        return self.portfolio.sell_coin(coin_symbol, quantity_usd, quantity_coin)
