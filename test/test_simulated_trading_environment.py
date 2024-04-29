import httpretty
import requests
import unittest

from trading_environments.simulated_trading_environment import SimulatedTradingEnvironment


simulated_trading_environment = SimulatedTradingEnvironment()

class TestSimulatedTradingEnvironment(unittest.TestCase):
    
    @httpretty.activate
    def test_get_price_returns_correct_value(self):
        
        ticker = "BTC"
        expected_price = 62944.77483424213
        base_url = "http://example.com"

        httpretty.register_uri(httpretty.GET, f"{base_url}/coins/single",
                               body=f'{{"rate": {expected_price}}}',
                               content_type="application/json")
        
        environment = SimulatedTradingEnvironment(base_url)

        price = environment.get_price(ticker)

        self.assertTrue(httpretty.has_request)
        self.assertEqual(price, expected_price)

        # TODO: Check details of request (request body needs to be correct)

if __name__ == '__main__':
    unittest.main()
