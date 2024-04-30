import os
import unittest
from dotenv import load_dotenv

from src.coin_api_adapters.livecoinwatch_adapter import LiveCoinWatchAdapter
from src.trading_environments.simulated_trading_environment import SimulatedTradingEnvironment


load_dotenv()

API_KEY = os.getenv('API_KEY')
BASE_URL = "https://api.livecoinwatch.com"
TICKER = "BTC"

coin_api = LiveCoinWatchAdapter(BASE_URL, API_KEY)
environment = SimulatedTradingEnvironment(coin_api)


class TestSimulatedTradingEnvironment(unittest.TestCase):
    
    def test_get_price_returns(self):
        
        price = environment.get_price(TICKER)
        self.assertIsNotNone(price)


if __name__ == '__main__':
    unittest.main()