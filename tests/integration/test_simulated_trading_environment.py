import csv
import os
import unittest
from dotenv import load_dotenv

from src.coin_api_adapters.livecoinwatch_adapter import LiveCoinWatchAdapter
from src.trading_environments.simulated_trading_environment import SimulatedTradingEnvironment


load_dotenv()

API_KEY = os.getenv('API_KEY')
BASE_URL = "https://api.livecoinwatch.com"
TICKER = "ETH"

coin_api = LiveCoinWatchAdapter(BASE_URL, API_KEY)
portfolio_path = os.path.join('tests', 'integration', 'fixtures', 'test_portfoilio.csv')

environment = SimulatedTradingEnvironment(coin_api, portfolio_path)


class TestSimulatedTradingEnvironment(unittest.TestCase):        
    
    def test_get_price_returns(self):
        
        price = environment.get_price(TICKER)
        self.assertIsNotNone(price)

    def test_buy_coin_adds_to_portfoilio(self):
        
        with open(portfolio_path, 'w', newline='') as file:
            csv_writer = csv.DictWriter(file, fieldnames=['Ticker', 'Quantity'])
            csv_writer.writerow({'Ticker':'USD', 'Quantity':1000.0})

        result = environment.buy_coin('ETH', 500)

        with open(portfolio_path, 'r', newline='') as file:
            csv_reader = csv.DictReader(file, fieldnames=['Ticker', 'Quantity'])
            portfolio = {}
            for row in csv_reader:
                portfolio[row['Ticker']] = float(row['Quantity'])
        
        self.assertEqual(500.0, portfolio['USD'])
        self.assertGreater(portfolio['ETH'], 0.0)
        self.assertTrue(result)
    
    def test_buy_coin_fails_when_not_enough_funds(self):
        
        with open(portfolio_path, 'w', newline='') as file:
            csv_writer = csv.DictWriter(file, fieldnames=['Ticker', 'Quantity'])
            csv_writer.writerow({'Ticker':'USD', 'Quantity':1000.0})

        result = environment.buy_coin('ETH', 5000)

        with open(portfolio_path, 'r', newline='') as file:
            csv_reader = csv.DictReader(file, fieldnames=['Ticker', 'Quantity'])
            portfolio = {}
            for row in csv_reader:
                portfolio[row['Ticker']] = float(row['Quantity'])
        
        self.assertEqual(1000.0, portfolio['USD'])
        self.assertFalse('ETH' in portfolio)
        self.assertFalse(result)
    
    def test_sell_coin_removes_from_portfolio(self):
        
        with open(portfolio_path, 'w', newline='') as file:
            csv_writer = csv.DictWriter(file, fieldnames=['Ticker', 'Quantity'])
            csv_writer.writerow({'Ticker':'USD', 'Quantity':0})
            csv_writer.writerow({'Ticker':'ETH', 'Quantity':500})

        result = environment.sell_coin('ETH', 500)

        with open(portfolio_path, 'r', newline='') as file:
            csv_reader = csv.DictReader(file, fieldnames=['Ticker', 'Quantity'])
            portfolio = {}
            for row in csv_reader:
                portfolio[row['Ticker']] = float(row['Quantity'])
        
        self.assertEqual(0.0, portfolio['ETH'])
        self.assertGreater(portfolio['USD'], 0.0)
        self.assertTrue(result)

    def test_sell_coin_fails_when_not_enough_funds(self):
        
        with open(portfolio_path, 'w', newline='') as file:
            csv_writer = csv.DictWriter(file,fieldnames=['Ticker', 'Quantity'])
            csv_writer.writerow({'Ticker':'USD', 'Quantity':0})
            csv_writer.writerow({'Ticker':'ETH', 'Quantity':500})

        result = environment.sell_coin('ETH', 5000)

        with open(portfolio_path, 'r', newline='') as file:
            csv_reader = csv.DictReader(file, fieldnames=['Ticker', 'Quantity'])
            portfolio = {}
            for row in csv_reader:
                portfolio[row['Ticker']] = float(row['Quantity'])
        
        self.assertEqual(0.0, portfolio['USD'])
        self.assertEqual(500.0, portfolio['ETH'])
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
