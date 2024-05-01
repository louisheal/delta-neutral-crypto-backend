import csv
import os
import unittest
from dotenv import load_dotenv
from pathlib import Path

from src.coin_api_adapters.livecoinwatch_adapter import LiveCoinWatchAdapter
from src.portfolios.csv_portfolio import CsvPortfolio
from src.trading_environments.simulated_trading_environment import SimulatedTradingEnvironment


load_dotenv()

API_KEY = os.getenv('API_KEY')
BASE_URL = "https://api.livecoinwatch.com"
TICKER = 'ETH'
PORTFOLIO_PATH = Path('tests/integration/fixtures/test_portfolio.csv')


class TestSimulatedTradingEnvironment(unittest.TestCase):

    def setUp(self) -> None:
       self.coin_api = LiveCoinWatchAdapter(BASE_URL, API_KEY)
       self.portfolio = CsvPortfolio(PORTFOLIO_PATH)
       self.environment = SimulatedTradingEnvironment(self.coin_api, self.portfolio)
    
    def test_get_price_returns(self):
        
        price = self.environment.get_price(TICKER)
        self.assertIsNotNone(price)

    def test_buy_coin_adds_to_portfoilio(self):
        
        self.__setup_buy_coin_tests()

        result = self.environment.buy_coin(TICKER, 500)
        quantity_usd = self.portfolio.get_quantity_usd()
        quantity_eth = self.portfolio.get_quantity_coin(TICKER)
        
        self.assertEqual(500.0, quantity_usd)
        self.assertGreater(quantity_eth, 0.0)
        self.assertTrue(result)
    
    def test_buy_coin_fails_when_not_enough_funds(self):
        
        self.__setup_buy_coin_tests()

        result = self.environment.buy_coin(TICKER, 5000)
        quantity_usd = self.portfolio.get_quantity_usd()
        quantity_eth = self.portfolio.get_quantity_coin(TICKER)
        
        self.assertEqual(1000.0, quantity_usd)
        self.assertEqual(0.0, quantity_eth)
        self.assertFalse(result)
    
    def test_sell_coin_removes_from_portfolio(self):
        
        self.__setup_sell_coin_tests()

        result = self.environment.sell_coin(TICKER, 500)
        quantity_usd = self.portfolio.get_quantity_usd()
        quantity_eth = self.portfolio.get_quantity_coin(TICKER)
        
        self.assertEqual(0.0, quantity_eth)
        self.assertGreater(quantity_usd, 0.0)
        self.assertTrue(result)

    def test_sell_coin_fails_when_not_enough_funds(self):
        
        self.__setup_sell_coin_tests()

        result = self.environment.sell_coin(TICKER, 5000)
        quantity_usd = self.portfolio.get_quantity_usd()
        quantity_eth = self.portfolio.get_quantity_coin(TICKER)
        
        self.assertEqual(0.0, quantity_usd)
        self.assertEqual(500.0, quantity_eth)
        self.assertFalse(result)
    
    def __setup_buy_coin_tests(self):
        
        portfolio = {
            'USD': 1000.0    
        }

        with open(PORTFOLIO_PATH, 'w') as file:
            csv_writer = csv.DictWriter(file, fieldnames=['Ticker','Quantity'])
            for k, v in portfolio.items():
                csv_writer.writerow({'Ticker':k, 'Quantity':v})
    
    def __setup_sell_coin_tests(self):
        
        portfolio = {
            'USD': 0.0,
            'ETH': 500.0
        }

        with open(PORTFOLIO_PATH, 'w') as file:
            csv_writer = csv.DictWriter(file, fieldnames=['Ticker','Quantity'])
            for k, v in portfolio.items():
                csv_writer.writerow({'Ticker':k, 'Quantity':v})


if __name__ == '__main__':
    unittest.main()
