import csv
from pathlib import Path

from .portfolio import IPortfolio


USD = 'USD'
TICKER = 'Ticker'
QUANTITY = 'Quantity'
FIELDNAMES = [TICKER, QUANTITY]


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

        portfolio[USD] = portfolio.get(USD, 0) - quantity_usd
        portfolio[coin_symbol] = portfolio.get(coin_symbol, 0) + quantity_coin

        return self.__save_portfolio(portfolio)
    
    def sell_coin(self, coin_symbol: str, quantity_usd: float, quantity_coin: float) -> bool:
        portfolio = self.__load_portfolio()

        portfolio[USD] = portfolio.get(USD, 0) + quantity_usd
        portfolio[coin_symbol] = portfolio.get(coin_symbol, 0) - quantity_coin

        return self.__save_portfolio(portfolio)
    
    def stake_coin(self, pool_id: str, symbol_one: float, symbol_two: float, quantity_one: float, quantity_two: float, quantity_lp_tokens: float) -> bool:
        portfolio = self.__load_portfolio()

        portfolio[symbol_one] = portfolio.get(symbol_one, 0) - quantity_one
        portfolio[symbol_two] = portfolio.get(symbol_two, 0) - quantity_two
        portfolio[pool_id] = portfolio.get(pool_id, 0) + quantity_lp_tokens

        return self.__save_portfolio(portfolio)

    def __load_portfolio(self) -> dict:
        
        with open(self.path, 'r', newline='') as file:
            csv_reader = csv.DictReader(file, fieldnames=FIELDNAMES)
            portfolio = {}
            for row in csv_reader:
                portfolio[row[TICKER]] = float(row[QUANTITY])

        return portfolio

    def __save_portfolio(self, portfolio: dict) -> bool:
        
        with open(self.path, 'w') as file:
            csv_writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            for k, v in portfolio.items():
                csv_writer.writerow({TICKER:k, QUANTITY:v})
        
        return True
    