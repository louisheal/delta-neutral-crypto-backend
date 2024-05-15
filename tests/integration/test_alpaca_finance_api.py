import os
import unittest
from dotenv import load_dotenv

from app.farming_pools.alpaca_finance_api import AlpacaFinanceApi


load_dotenv()

ALPACA_FINANCE_URL = os.getenv('ALPACA_FINANCE_URL')

POOL_ID = "pcs-usdt-bnb"
INVALID_POOL_ID = "INVALID POOL ID"


class TestAlpacaFinanceApi(unittest.TestCase):
    
    def setUp(self) -> None:
        self.af_api = AlpacaFinanceApi(ALPACA_FINANCE_URL)

    def test_get_pools_is_not_empty(self):
        pools = self.af_api.get_pools()
        self.assertGreater(len(pools), 0)

    def test_get_pool_by_id_is_not_none(self):
        pool = self.af_api.get_pool_by_id(POOL_ID)
        self.assertIsNotNone(pool)

    def test_get_pool_by_id_returns_none_for_invalid_id(self):
        pool = self.af_api.get_pool_by_id(INVALID_POOL_ID)
        self.assertIsNone(pool)
