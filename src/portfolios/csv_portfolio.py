import csv
from pathlib import Path

import math

from .portfolio import IPortfolio


FIELDNAMES = ['Ticker', 'Quantity']
USD = 'USD'


class CsvPortfolio(IPortfolio):
    
    def __init__(self, path: Path) -> None:
        self.path = path

    def get_quantity_usd(self) -> float:
        portfolio = self.__load_portfolio()
        return portfolio.get(USD, 0)
    
    def get_quantity_coin(self, coin_symbol: str) -> float:
        portfolio = self.__load_portfolio()
        return portfolio.get(coin_symbol, 0)
    
    def buy_coin(self, coin_symbol: str, quantity_usd: float, quantity_coin: float) -> bool:
        portfolio = self.__load_portfolio()

        portfolio[USD] -= quantity_usd
        portfolio[coin_symbol] = portfolio.get(coin_symbol, 0) + quantity_coin

        return self.__save_portfolio(portfolio)
    
    def sell_coin(self, coin_symbol: str, quantity_usd: float, quantity_coin: float) -> bool:
        portfolio = self.__load_portfolio()

        portfolio[USD] += quantity_usd
        portfolio[coin_symbol] = portfolio.get(coin_symbol, 0) - quantity_coin

        return self.__save_portfolio(portfolio)
    
    def stake_coin(self, pool_id: str, amount0: float, amount1: float) -> bool:
        pass
    
    # TODO
    def unstake_coin(self):
        pass

    def __load_portfolio(self) -> dict:
        
        with open(self.path, 'r', newline='') as file:
            csv_reader = csv.DictReader(file, fieldnames=FIELDNAMES)
            portfolio = {}
            for row in csv_reader:
                portfolio[row['Ticker']] = float(row['Quantity'])

        return portfolio

    def __save_portfolio(self, portfolio: dict) -> bool:
        
        with open(self.path, 'w') as file:
            csv_writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            for k, v in portfolio.items():
                csv_writer.writerow({'Ticker':k, 'Quantity':v})
        
        return True
    