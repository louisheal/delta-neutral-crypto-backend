import unittest
from unittest.mock import MagicMock

from src.coin_api_adapters.coin_api_adapter import ICoinApiAdapter
from src.portfolios.portfolio import IPortfolio
from src.trading_environments.simulated_trading_environment import SimulatedTradingEnvironment


PRICE = 50.0
COIN_SYMBOL = 'ETH'
QUANTITY_USD = 100.0


class TestSimulatedTradingEnvironment(unittest.TestCase):
    
    def setUp(self) -> None:
        self.mock_coin_api = MagicMock(spec=ICoinApiAdapter)
        self.mock_portfolio = MagicMock(spec=IPortfolio)
        self.environment = SimulatedTradingEnvironment(self.mock_coin_api, self.mock_portfolio)
    
    def test_get_price_returns_correct_value(self):

        self.mock_coin_api.get_price.return_value = PRICE

        price = self.environment.get_price(COIN_SYMBOL)

        self.assertEqual(price, PRICE)
        self.mock_coin_api.get_price.assert_called_once_with(COIN_SYMBOL)

    def test_buy_coin_calls_portfolio_with_correct_values(self):
        
        self.mock_coin_api.get_price.return_value = PRICE
        self.mock_portfolio.get_quantity_usd.return_value = QUANTITY_USD
        self.mock_portfolio.buy_coin.return_value = True

        result = self.environment.buy_coin(COIN_SYMBOL, QUANTITY_USD)
        
        self.assertTrue(result)
        self.mock_coin_api.get_price.assert_called_once_with(COIN_SYMBOL)
        self.mock_portfolio.get_quantity_usd.assert_called_once()
        self.mock_portfolio.buy_coin.assert_called_once_with(COIN_SYMBOL, QUANTITY_USD, QUANTITY_USD / PRICE)
    
    def test_buy_coin_returns_false_when_insufficient_funds(self):
        
        self.mock_portfolio.get_quantity_usd.return_value = 0.0
        
        result = self.environment.buy_coin(COIN_SYMBOL, QUANTITY_USD)
        
        self.assertFalse(result)
        self.mock_portfolio.get_quantity_usd.assert_called_once()
    
    def test_sell_coin_calls_portfolio_with_correct_values(self):
        
        self.mock_coin_api.get_price.return_value = PRICE
        self.mock_portfolio.get_quantity_coin.return_value = QUANTITY_USD / PRICE
        self.mock_portfolio.sell_coin.return_value = True

        result = self.environment.sell_coin(COIN_SYMBOL, QUANTITY_USD / PRICE)
        
        self.assertTrue(result)
        self.mock_coin_api.get_price.assert_called_once_with(COIN_SYMBOL)
        self.mock_portfolio.get_quantity_coin.assert_called_once_with(COIN_SYMBOL)
        self.mock_portfolio.sell_coin.assert_called_with(COIN_SYMBOL, QUANTITY_USD, QUANTITY_USD / PRICE)
    
    def test_sell_coin_returns_false_when_insufficient_funds(self):
        
        self.mock_portfolio.get_quantity_coin.return_value = 0.0

        result = self.environment.sell_coin(COIN_SYMBOL, QUANTITY_USD)
        
        self.assertFalse(result)
        self.mock_portfolio.get_quantity_coin.assert_called_once_with(COIN_SYMBOL)


if __name__ == '__main__':
    unittest.main()
