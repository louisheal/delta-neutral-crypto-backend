import httpretty
import json
import os
import unittest
from dotenv import load_dotenv

from src.farming_platforms.alpaca_finance_api import AlpacaFinanceApi


load_dotenv()

URL = os.getenv('ALPACA_FINANCE_URL')

DATA = 'data'
FARMING_POOLS = 'farmingPools'
SOURCE_NAME = 'sourceName'
TRADING_FEE_APR = 'tradingFeeApr'
BORROWING_INTERESTS = 'borrowingInterests'
INTEREST_PERCENT = 'interestPercent'

POOL_NAME = "POOL NAME"
TRADING_FEE = 123
BORROW_RATE_ONE = 123
BORROW_RATE_TWO = 456

POOL_BODY = {
    DATA: {
        FARMING_POOLS: [{
                SOURCE_NAME: POOL_NAME,
                TRADING_FEE_APR: TRADING_FEE,
                BORROWING_INTERESTS: [
                    { INTEREST_PERCENT: BORROW_RATE_ONE },
                    { INTEREST_PERCENT: BORROW_RATE_TWO }
                ]
        }]
}}


class TestAlpacaFinanceApi(unittest.TestCase):
    
    def setUp(self) -> None:
        self.af_api = AlpacaFinanceApi()

    @httpretty.activate
    def test_get_pools_TODO(self):
        
        httpretty.register_uri(httpretty.GET, URL,
                               body=json.dumps(POOL_BODY),
                               content_type='application/json')

        pools = self.af_api.get_pools()
        pool = pools[0]

        self.assertTrue(httpretty.has_request)
        self.assertEqual(pool.pool_name, POOL_NAME)
        self.assertEqual(pool.trading_fee, TRADING_FEE)
        self.assertEqual(pool.borrow_rate_one, BORROW_RATE_ONE)
        self.assertEqual(pool.borrow_rate_two, BORROW_RATE_TWO)
