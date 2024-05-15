import unittest

from app.farming_pools.alpaca_finance_pool import AlpacaFinancePool


class TestAlpacaFinanceApi(unittest.TestCase):
    
    def setUp(self) -> None:
        self.af_api = AlpacaFinancePool()

    def test_get_pools_is_not_empty(self):
        pools = self.af_api.get_pools()
        self.assertGreater(len(pools), 0)
