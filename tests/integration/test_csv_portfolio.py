import csv
import unittest
from pathlib import Path

from src.portfolios.csv_portfolio import CsvPortfolio


PATH = Path("tests/integration/fixtures/test_portfolio.csv")

TICKER = 'Ticker'
QUANTITY = 'Quantity'
FIELDNAMES = [TICKER, QUANTITY]

QUANTITY_USD = 1000.00
QUANTITY_COIN_ONE = 0.123
QUANTITY_COIN_TWO = 0.456
QUANTITY_LP_TOKENS = 5.0
PAIR_ID = 'PAIR_ID'

USD = 'USD'
COIN_ONE = 'COIN_ONE'
COIN_TWO = 'COIN_TWO'


class TestCsvPortfolio(unittest.TestCase):
    
    def setUp(self) -> None:
        self.csv_portfolio = CsvPortfolio(PATH)
    
    def test_get_quantity_usd(self):
        self.__setup_tests()

        quantity_usd = self.csv_portfolio.get_quantity_usd()
        self.assertEqual(quantity_usd, QUANTITY_USD)
    
    def test_get_quantity_coin(self):
        self.__setup_tests()

        quantity_coin = self.csv_portfolio.get_quantity_coin(COIN_ONE)
        self.assertEqual(quantity_coin, QUANTITY_COIN_ONE)
    
    def test_buy_coin(self):
        self.__setup_tests()

        result = self.csv_portfolio.buy_coin(COIN_ONE, QUANTITY_USD, QUANTITY_COIN_ONE)
        amount_usd = self.csv_portfolio.get_quantity_usd()
        amount_coin = self.csv_portfolio.get_quantity_coin(COIN_ONE)

        self.assertEqual(amount_usd, 0.0)
        self.assertEqual(amount_coin, 2 * QUANTITY_COIN_ONE)
        self.assertTrue(result)
    
    def test_sell_coin(self):
        self.__setup_tests()

        result = self.csv_portfolio.sell_coin(COIN_ONE, QUANTITY_USD, QUANTITY_COIN_ONE)
        amount_usd = self.csv_portfolio.get_quantity_usd()
        amount_coin = self.csv_portfolio.get_quantity_coin(COIN_ONE)

        self.assertEqual(amount_usd, 2 * QUANTITY_USD)
        self.assertEqual(amount_coin, 0.0)
        self.assertTrue(result)
    
    def test_stake_coin(self):
        self.__setup_tests()

        result = self.csv_portfolio.stake_coin(PAIR_ID, COIN_ONE, COIN_TWO, QUANTITY_COIN_ONE, QUANTITY_COIN_TWO, QUANTITY_LP_TOKENS)
        amount_coin_one = self.csv_portfolio.get_quantity_coin(COIN_ONE)
        amount_coin_two = self.csv_portfolio.get_quantity_coin(COIN_TWO)
        amount_lp_tokens = self.csv_portfolio.get_quantity_coin(PAIR_ID)

        self.assertEqual(amount_coin_one, 0.0)
        self.assertEqual(amount_coin_two, 0.0)
        self.assertEqual(amount_lp_tokens, QUANTITY_LP_TOKENS)
        self.assertTrue(result)
    
    def __setup_tests(self):
        portfolio = {
            USD: QUANTITY_USD,
            COIN_ONE: QUANTITY_COIN_ONE,
            COIN_TWO: QUANTITY_COIN_TWO
        }
        self.__save_portfolio(portfolio)

    # TODO: Move to tests/utils.py
    def __save_portfolio(self, portfolio: dict):
        
         with open(PATH, 'w') as file:
            csv_writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            for k, v in portfolio.items():
                csv_writer.writerow({'Ticker':k, 'Quantity':v})
