import httpretty
import unittest

from src.liquidity_pool_apis.uniswap_api import UniswapApi


API_KEY = 'API_KEY'
APP_ID = 'UNISWAP_APP_ID'
URL = 'https://example.com'

RESERVE_0 = 123
RESERVE_1 = 456
SYMBOL_0 = "SYMBOL_0"
SYMBOL_1 = "SYMBOL_1"
TOTAL_SUPPLY = 789

PAIR_ID = 'PAIR_ID'

class TestUniswapApi(unittest.TestCase):
    
    def setUp(self) -> None:
        self.uniswap_api = UniswapApi(URL, API_KEY, APP_ID)
    
    @httpretty.activate
    def test_get_pair_calls_endpoint_with_correct_data(self):
        
        httpretty.register_uri(httpretty.POST,
                               f"{URL}/api/{API_KEY}/subgraphs/id/{APP_ID}",
                               body=f'''{{
                                    "data": {{
                                        "pair": {{
                                            "id": "{PAIR_ID}",
                                            "reserve0": "{RESERVE_0}",
                                            "reserve1": "{RESERVE_1}",
                                            "token0": {{"symbol": "{SYMBOL_0}"}},
                                            "token1": {{"symbol": "{SYMBOL_1}"}},
                                            "totalSupply": "{TOTAL_SUPPLY}"
                                        }}
                                    }}
                                }}''',
                               content_type="application/json")
    
        pair = self.uniswap_api.get_pair(PAIR_ID)

        self.assertTrue(httpretty.has_request)

        self.assertEqual(pair.pair_id, PAIR_ID)
        self.assertEqual(pair.reserve0, RESERVE_0)
        self.assertEqual(pair.reserve1, RESERVE_1)
        self.assertEqual(pair.symbol0, SYMBOL_0)
        self.assertEqual(pair.symbol1, SYMBOL_1)
        self.assertEqual(pair.total_supply, TOTAL_SUPPLY)
