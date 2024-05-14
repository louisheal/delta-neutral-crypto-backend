import unittest

from src.farming_platforms.alpaca_finance_api import AlpacaFinanceApi


class TestAlpacaFinanceApi(unittest.TestCase):
    
    def setUp(self) -> None:
        self.af_api = AlpacaFinanceApi()
