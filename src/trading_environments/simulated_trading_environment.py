import csv
import os

from ..coin_api_adapters.coin_api_adapter import ICoinApiAdapter
from .trading_environment import ITradingEnvironment


class SimulatedTradingEnvironment(ITradingEnvironment):
    
    def __init__(self, coin_api: ICoinApiAdapter, portfolio_path: os.path):
        self.coin_api = coin_api
        self.portfolio_path = portfolio_path
    
    def get_price(self, coin_symbol: str) -> float:
        return self.coin_api.get_price(coin_symbol)
    
    # TODO: Handle incorrect coin_symbol
    def buy_coin(self, coin_symbol: str, quantity_usd: int) -> bool:
        with open(self.portfolio_path, 'r') as file:
            csv_reader = csv.DictReader(file, fieldnames=['Ticker', 'Quantity'])

            portfolio = {}
            for row in csv_reader:
                portfolio[row['Ticker']] = float(row['Quantity'])

        if portfolio['USD'] < quantity_usd:
            return False
        
        portfolio['USD'] -= quantity_usd
        if coin_symbol in portfolio:
            portfolio[coin_symbol] += quantity_usd / self.get_price(coin_symbol)
        else:
            portfolio[coin_symbol] = quantity_usd / self.get_price(coin_symbol)

        with open(self.portfolio_path, 'w') as file:
            csv_writer = csv.DictWriter(file, fieldnames=['Ticker', 'Quantity'])
            for k, v in portfolio.items():
                csv_writer.writerow({'Ticker':k, 'Quantity':v})

        return True
    
    # TODO: Handle incorrect coin_symbol
    def sell_coin(self, coin_symbol: str, quantity_coin: int) -> bool:
        with open(self.portfolio_path, 'r') as file:
            csv_reader = csv.DictReader(file, fieldnames=['Ticker', 'Quantity'])

            portfolio = {}
            for row in csv_reader:
                portfolio[row['Ticker']] = float(row['Quantity'])
        
        if portfolio[coin_symbol] < quantity_coin:
            return False
        
        portfolio[coin_symbol] -= quantity_coin
        portfolio['USD'] += quantity_coin * self.get_price(coin_symbol)

        with open(self.portfolio_path, 'w') as file:
            csv_writer = csv.DictWriter(file, fieldnames=['Ticker', 'Quantity'])
            for k, v in portfolio.items():
                csv_writer.writerow({'Ticker':k, 'Quantity':v})

        return True
