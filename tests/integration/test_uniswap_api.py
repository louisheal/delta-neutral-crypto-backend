import os
import unittest
from dotenv import load_dotenv

from src.liquidity_pool_apis.uniswap_api import UniswapApi


load_dotenv()

API_KEY = os.getenv('GRAPH_API_KEY')
APP_ID = os.getenv('UNISWAP_APP_ID')
URL = os.getenv('GRAPH_URL')

PAIR_ID = "0xa478c2975ab1ea89e8196811f51a7b7ade33eb11"


class TestUniswapApi(unittest.TestCase):
    
    def setUp(self) -> None:
        self.uniswap_api = UniswapApi(URL, API_KEY, APP_ID)
    
    def test_get_pair_returns_values(self):
        
        pair = self.uniswap_api.get_pair(PAIR_ID)

        self.assertIsNotNone(pair.pair_id)
        self.assertIsNotNone(pair.total_supply)
        self.assertIsNotNone(pair.reserve0)
        self.assertIsNotNone(pair.reserve1)
        self.assertIsNotNone(pair.symbol0)
        self.assertIsNotNone(pair.symbol1)
        