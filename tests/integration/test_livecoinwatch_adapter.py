import os
import unittest
from dotenv import load_dotenv

from src.coin_api_adapters.livecoinwatch_adapter import LiveCoinWatchAdapter


load_dotenv()

BASE_URL = "https://api.livecoinwatch.com"
API_KEY = os.getenv('API_KEY')
COIN_TICKER = "BTC"

coin_api = LiveCoinWatchAdapter(BASE_URL, API_KEY)


class TestLiveCoinWatchAdapter(unittest.TestCase):
    
    def test_get_price_calls_api_and_returns_price(self):
        
        price = coin_api.get_price(COIN_TICKER)
        self.assertIsNotNone(price)


if __name__ == '__main__':
    unittest.main()
