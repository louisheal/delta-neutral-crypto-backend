import unittest
from unittest.mock import MagicMock

from src.coin_api_adapters.coin_api_adapter import ICoinApiAdapter
from src.trading_environments.simulated_trading_environment import SimulatedTradingEnvironment


PRICE = 123.456789
TICKER = "BTC"


class TestSimulatedTradingEnvironment(unittest.TestCase):
    
    def test_get_price_returns_correct_value(self):
        
        coin_api = ICoinApiAdapter()
        coin_api.get_price = MagicMock(return_value=PRICE)

        environment = SimulatedTradingEnvironment(coin_api)
        price = environment.get_price(TICKER)

        self.assertEqual(price, PRICE)
        # TODO: Assert coin_api.get_price(ticker) was called


if __name__ == '__main__':
    unittest.main()
