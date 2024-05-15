import httpretty
import json
import unittest

from app.farming_pools.alpaca_finance_api import AlpacaFinanceApi


URL = "https://example.com"

DATA = 'data'
FARMING_POOLS = 'farmingPools'

KEY = 'key'
SOURCE_NAME = 'sourceName'
TRADING_FEE_APR = 'tradingFeeApr'
BORROWING_INTERESTS = 'borrowingInterests'
INTEREST_PERCENT = 'interestPercent'
WORKING_TOKEN = 'workingToken'
TOKEN_A = 'tokenA'
TOKEN_B = 'tokenB'
SYMBOL = 'symbol'

POOL_ID = 1
POOL_NAME = "POOL NAME"
TOKEN_ONE = "TOKEN ONE"
TOKEN_TWO = "TOKEN TWO"
TRADING_FEE = 123
BORROW_RATE_ONE = 123
BORROW_RATE_TWO = 456

INVALID_POOL_ID = "INVALID POOL ID"

POOL_BODY = {
    DATA: {
        FARMING_POOLS: [{
                KEY: POOL_ID,
                SOURCE_NAME: POOL_NAME,
                TRADING_FEE_APR: TRADING_FEE,
                BORROWING_INTERESTS: [
                    { INTEREST_PERCENT: BORROW_RATE_ONE },
                    { INTEREST_PERCENT: BORROW_RATE_TWO }
                ],
                WORKING_TOKEN: {
                    TOKEN_A: { SYMBOL: TOKEN_ONE },
                    TOKEN_B: { SYMBOL: TOKEN_TWO }
                }
        }]
}}


class TestAlpacaFinanceApi(unittest.TestCase):
    
    def setUp(self) -> None:
        self.af_api = AlpacaFinanceApi(URL)

    @httpretty.activate
    def test_get_pools_returns_pool(self):
        
        httpretty.register_uri(httpretty.GET, URL,
                               body=json.dumps(POOL_BODY),
                               content_type='application/json')

        pools = self.af_api.get_pools()
        pool = pools[0]

        self.assertTrue(httpretty.has_request)
        self.assertEqual(pool.pool_id, POOL_ID)
        self.assertEqual(pool.pool_name, POOL_NAME)
        self.assertEqual(pool.token_one_symbol, TOKEN_ONE)
        self.assertEqual(pool.token_two_symbol, TOKEN_TWO)
        self.assertEqual(pool.trading_fee, TRADING_FEE)
        self.assertEqual(pool.borrow_rate_one, BORROW_RATE_ONE)
        self.assertEqual(pool.borrow_rate_two, BORROW_RATE_TWO)

    @httpretty.activate
    def test_get_pools_by_id_returns_correct_pool(self):
        
        httpretty.register_uri(httpretty.GET, URL,
                               body=json.dumps(POOL_BODY),
                               content_type='application/json')

        pool = self.af_api.get_pool_by_id(POOL_ID)

        self.assertTrue(httpretty.has_request)
        self.assertEqual(pool.pool_id, POOL_ID)
        self.assertEqual(pool.pool_name, POOL_NAME)
        self.assertEqual(pool.token_one_symbol, TOKEN_ONE)
        self.assertEqual(pool.token_two_symbol, TOKEN_TWO)
        self.assertEqual(pool.trading_fee, TRADING_FEE)
        self.assertEqual(pool.borrow_rate_one, BORROW_RATE_ONE)
        self.assertEqual(pool.borrow_rate_two, BORROW_RATE_TWO)

    @httpretty.activate
    def test_get_pool_by_id_returns_none_for_invalid_id(self):
        
        httpretty.register_uri(httpretty.GET, URL,
                               body=json.dumps(POOL_BODY),
                               content_type='application/json')
        
        pool = self.af_api.get_pool_by_id(INVALID_POOL_ID)

        self.assertTrue(httpretty.has_request)
        self.assertIsNone(pool)
