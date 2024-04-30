import os
import unittest
from dotenv import load_dotenv

from src.trading_environments.simulated_trading_environment import SimulatedTradingEnvironment


load_dotenv()

BASE_URL = "https://api.livecoinwatch.com"
API_KEY = os.getenv('API_KEY')
COIN_TICKER = "BTC"


class TestSimulatedTradingEnvironment(unittest.TestCase):
    
    def test_get_price_calls_api_and_returns_price(self):
        environment = SimulatedTradingEnvironment(BASE_URL, API_KEY)
        price = environment.get_price(COIN_TICKER)
        self.assertIsNotNone(price)


if __name__ == '__main__':
    unittest.main()
