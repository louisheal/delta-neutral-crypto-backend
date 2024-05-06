import csv
import os
import unittest
from dotenv import load_dotenv
from pathlib import Path

from src.coin_api_adapters.livecoinwatch_adapter import LiveCoinWatchAdapter
from src.liquidity_pool_apis.uniswap_api import UniswapApi
from src.portfolios.csv_portfolio import CsvPortfolio
from src.trading_environments.simulated_trading_environment import SimulatedTradingEnvironment


load_dotenv()

COIN_URL = os.getenv('COIN_URL')
COIN_API_KEY = os.getenv('COIN_API_KEY')

GRAPH_URL = os.getenv('GRAPH_URL')
GRAPH_API_KEY = os.getenv('GRAPH_API_KEY')
UNISWAP_APP_ID = os.getenv('UNISWAP_APP_ID')

PORTFOLIO_PATH = Path('tests/integration/fixtures/test_portfolio.csv')

TICKER = 'Ticker'
QUANTITY = 'Quantity'
FIELDNAMES = [TICKER,QUANTITY]

USD = 'USD'
ETH = 'ETH'


class TestSimulatedTradingEnvironment(unittest.TestCase):

    def setUp(self):
       self.coin_api = LiveCoinWatchAdapter(COIN_URL, COIN_API_KEY)
       self.pool_api = UniswapApi(GRAPH_URL, GRAPH_API_KEY, UNISWAP_APP_ID)
       self.portfolio = CsvPortfolio(PORTFOLIO_PATH)
       self.environment = SimulatedTradingEnvironment(self.coin_api, self.pool_api, self.portfolio)
    
    def test_get_price_returns(self):
        price = self.environment.get_price(ETH)
        self.assertIsNotNone(price)

    def test_buy_coin_adds_to_portfoilio(self):
        self.__setup_buy_coin_tests()

        result = self.environment.buy_coin(ETH, 500)
        quantity_usd = self.portfolio.get_quantity_usd()
        quantity_eth = self.portfolio.get_quantity_coin(ETH)
        
        self.assertEqual(500.0, quantity_usd)
        self.assertGreater(quantity_eth, 0.0)
        self.assertTrue(result)
    
    def test_buy_coin_fails_when_not_enough_funds(self):
        self.__setup_buy_coin_tests()

        result = self.environment.buy_coin(ETH, 5000)
        quantity_usd = self.portfolio.get_quantity_usd()
        quantity_eth = self.portfolio.get_quantity_coin(ETH)
        
        self.assertEqual(1000.0, quantity_usd)
        self.assertEqual(0.0, quantity_eth)
        self.assertFalse(result)
    
    def test_sell_coin_removes_from_portfolio(self):
        self.__setup_sell_coin_tests()

        result = self.environment.sell_coin(ETH, 500)
        quantity_usd = self.portfolio.get_quantity_usd()
        quantity_eth = self.portfolio.get_quantity_coin(ETH)
        
        self.assertEqual(0.0, quantity_eth)
        self.assertGreater(quantity_usd, 0.0)
        self.assertTrue(result)

    def test_sell_coin_fails_when_not_enough_funds(self):
        self.__setup_sell_coin_tests()

        result = self.environment.sell_coin(ETH, 5000)
        quantity_usd = self.portfolio.get_quantity_usd()
        quantity_eth = self.portfolio.get_quantity_coin(ETH)
        
        self.assertEqual(0.0, quantity_usd)
        self.assertEqual(500.0, quantity_eth)
        self.assertFalse(result)

    def test_stake_coin_adds_lp_tokens_to_portfolio(self):
        self.__setup_stake_coin_tests()
    
    def __setup_buy_coin_tests(self):
        portfolio = {
            USD: 1000.0 
        }
        self.__save_portfolio(portfolio)
    
    def __setup_sell_coin_tests(self):
        portfolio = {
            USD: 0.0,
            ETH: 500.0
        }
        self.__save_portfolio(portfolio)

    def __setup_stake_coin_tests(self):
        portfolio = {
            USD: 100.0,
            ETH: 500.0
        }
        self.__save_portfolio(portfolio)

    def __save_portfolio(self, portfolio: dict):
        
         with open(PORTFOLIO_PATH, 'w') as file:
            csv_writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            for k, v in portfolio.items():
                csv_writer.writerow({TICKER:k,QUANTITY:v})


if __name__ == '__main__':
    unittest.main()
