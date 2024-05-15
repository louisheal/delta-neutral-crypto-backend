import os
import unittest
from dotenv import load_dotenv

from app.coin_api_adapters.livecoinwatch_adapter import LiveCoinWatchAdapter


load_dotenv()

BASE_URL = os.getenv('COIN_URL')
API_KEY = os.getenv('COIN_API_KEY')
COIN_SYMBOL = 'ETH'

coin_api = LiveCoinWatchAdapter(BASE_URL, API_KEY)


class TestLiveCoinWatchAdapter(unittest.TestCase):
    
    def test_get_price_calls_api_and_returns_price(self):
        
        price = coin_api.get_price(COIN_SYMBOL)
        self.assertIsNotNone(price)


if __name__ == '__main__':
    unittest.main()
