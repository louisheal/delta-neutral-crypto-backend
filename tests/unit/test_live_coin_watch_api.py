import httpretty
import unittest

from app.coin_apis.live_coin_watch_api import LiveCoinWatchApi


API_KEY = "XXXXXX"
PRICE = 123.456789
TICKER = "BTC"
URL = "http://example.com"


class TestSimulatedTradingEnvironment(unittest.TestCase):
    
    @httpretty.activate
    def test_get_price_returns_correct_value(self):

        httpretty.register_uri(httpretty.POST, f"{URL}/coins/single",
                               body=f'{{"rate": {PRICE}}}',
                               content_type="application/json")
        
        coin_api = LiveCoinWatchApi(URL, API_KEY)

        price = coin_api.get_price_by_symbol(TICKER)

        self.assertTrue(httpretty.has_request)
        self.assertEqual(price, PRICE)

        request = httpretty.last_request()
        api_key = request.headers.get('x-api-key')
        ticker = request.parsed_body['code']

        self.assertEqual(api_key, API_KEY)
        self.assertEqual(ticker, TICKER)
