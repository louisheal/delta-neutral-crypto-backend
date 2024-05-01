import os

from ..coin_api_adapters.coin_api_adapter import ICoinApiAdapter
from .trading_environment import ITradingEnvironment
from ..utils import load_portfolio, save_portfolio


class SimulatedTradingEnvironment(ITradingEnvironment):
    
    def __init__(self, coin_api: ICoinApiAdapter, portfolio_path: os.path):
        self.coin_api = coin_api
        self.portfolio_path = portfolio_path
    
    def get_price(self, coin_symbol: str) -> float:
        return self.coin_api.get_price(coin_symbol)
    
    def buy_coin(self, coin_symbol: str, quantity_usd: int) -> bool:
        
        portfolio = load_portfolio(self.portfolio_path)

        if portfolio['USD'] < quantity_usd:
            return False
        
        portfolio['USD'] -= quantity_usd
        quantity_coin_bought = quantity_usd / self.get_price(coin_symbol)
        portfolio[coin_symbol] = portfolio.get(coin_symbol, 0) + quantity_coin_bought

        save_portfolio(portfolio, self.portfolio_path)

        return True
    
    def sell_coin(self, coin_symbol: str, quantity_coin: int) -> bool:
        
        portfolio = load_portfolio(self.portfolio_path)
        
        if portfolio[coin_symbol] < quantity_coin:
            return False
        
        portfolio[coin_symbol] -= quantity_coin
        portfolio['USD'] += quantity_coin * self.get_price(coin_symbol)

        save_portfolio(portfolio, self.portfolio_path)

        return True
