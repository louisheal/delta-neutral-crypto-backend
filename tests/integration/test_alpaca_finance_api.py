import unittest

from app.farming_platforms.alpaca_finance_api import AlpacaFinanceApi


class TestAlpacaFinanceApi(unittest.TestCase):
    
    def setUp(self) -> None:
        self.af_api = AlpacaFinanceApi()

    def test_get_pools_is_not_empty(self):
        pools = self.af_api.get_pools()
        self.assertGreater(len(pools), 0)
