import unittest
from unittest.mock import MagicMock, call

from src.coin_api_adapters.coin_api_adapter import ICoinApiAdapter
from src.liquidity_pool_apis.pair import Pair
from src.liquidity_pool_apis.liquidity_pool_api import ILiquidityPoolApi
from src.portfolios.portfolio import IPortfolio
from src.trading_environments.simulated_trading_environment import SimulatedTradingEnvironment


PRICE = 50.0
COIN_SYMBOL = 'ETH'
QUANTITY_USD = 100.0

AMOUNT_0 = 1
AMOUNT_1 = 64
LP_TOKENS = 10
NO_SUPPLY_TOKENS = 8

PAIR_ID = 'PAIR_ID'
TOTAL_SUPPLY = 100
RESERVE_0 = 10
RESERVE_1 = 640
SYMBOL_0 = 'USDT'
SYMBOL_1 = 'WETH'

PAIR = Pair(PAIR_ID, TOTAL_SUPPLY, RESERVE_0, RESERVE_1, SYMBOL_0, SYMBOL_1)
PAIR_NO_SUPPLY = Pair(PAIR_ID, 0, RESERVE_0, RESERVE_1, SYMBOL_0, SYMBOL_1)


class TestSimulatedTradingEnvironment(unittest.TestCase):
    
    def setUp(self) -> None:
        self.mock_coin_api = MagicMock(spec=ICoinApiAdapter)
        self.mock_pool_api = MagicMock(spec=ILiquidityPoolApi)
        self.mock_portfolio = MagicMock(spec=IPortfolio)
        self.environment = SimulatedTradingEnvironment(self.mock_coin_api, self.mock_pool_api, self.mock_portfolio)
    
    def test_get_price_returns_correct_value(self):

        self.mock_coin_api.get_price.return_value = PRICE

        price = self.environment.get_price(COIN_SYMBOL)

        self.mock_coin_api.get_price.assert_called_once_with(COIN_SYMBOL)
        self.assertEqual(price, PRICE)

    def test_buy_coin_calls_portfolio_with_correct_values(self):
        
        self.mock_coin_api.get_price.return_value = PRICE
        self.mock_portfolio.get_quantity_usd.return_value = QUANTITY_USD
        self.mock_portfolio.buy_coin.return_value = True

        result = self.environment.buy_coin(COIN_SYMBOL, QUANTITY_USD)
        
        self.mock_coin_api.get_price.assert_called_once_with(COIN_SYMBOL)
        self.mock_portfolio.get_quantity_usd.assert_called_once()
        self.mock_portfolio.buy_coin.assert_called_once_with(COIN_SYMBOL, QUANTITY_USD, QUANTITY_USD / PRICE)
        self.assertTrue(result)
    
    def test_buy_coin_returns_false_when_insufficient_funds(self):
        
        self.mock_portfolio.get_quantity_usd.return_value = 0.0
        
        result = self.environment.buy_coin(COIN_SYMBOL, QUANTITY_USD)
        
        self.mock_portfolio.get_quantity_usd.assert_called_once()
        self.assertFalse(result)
    
    def test_sell_coin_calls_portfolio_with_correct_values(self):
        
        self.mock_coin_api.get_price.return_value = PRICE
        self.mock_portfolio.get_quantity_coin.return_value = QUANTITY_USD / PRICE
        self.mock_portfolio.sell_coin.return_value = True

        result = self.environment.sell_coin(COIN_SYMBOL, QUANTITY_USD / PRICE)
        
        self.mock_coin_api.get_price.assert_called_once_with(COIN_SYMBOL)
        self.mock_portfolio.get_quantity_coin.assert_called_once_with(COIN_SYMBOL)
        self.mock_portfolio.sell_coin.assert_called_once_with(COIN_SYMBOL, QUANTITY_USD, QUANTITY_USD / PRICE)
        self.assertTrue(result)
    
    def test_sell_coin_returns_false_when_insufficient_funds(self):
        
        self.mock_portfolio.get_quantity_coin.return_value = 0.0

        result = self.environment.sell_coin(COIN_SYMBOL, QUANTITY_USD)
        
        self.mock_portfolio.get_quantity_coin.assert_called_once_with(COIN_SYMBOL)
        self.assertFalse(result)

    def test_stake_coin_calculates_lp_tokens_when_supply_greater_than_zero(self):
        
        self.mock_pool_api.get_pair.return_value = PAIR
        # TODO: Move to function
        self.mock_portfolio.get_quantity_coin.side_effect = lambda x: AMOUNT_0 if x == SYMBOL_0 else AMOUNT_1 if x == SYMBOL_1 else 'ERROR'

        result = self.environment.stake_coin(PAIR_ID, AMOUNT_0, AMOUNT_1)


        self.mock_pool_api.get_pair.assert_called_once_with(PAIR_ID)
        self.mock_portfolio.get_quantity_coin.assert_has_calls([call(SYMBOL_0), call(SYMBOL_1)])
        self.mock_portfolio.stake_coin.assert_called_once_with(PAIR_ID, SYMBOL_0, SYMBOL_1, AMOUNT_0, AMOUNT_1, LP_TOKENS)
        self.assertTrue(result)

    def test_stake_coin_calculates_lp_tokens_when_supply_is_zero(self):
        
        self.mock_pool_api.get_pair.return_value = PAIR_NO_SUPPLY
        self.mock_portfolio.get_quantity_coin.side_effect = lambda x: AMOUNT_0 if x == SYMBOL_0 else AMOUNT_1 if x == SYMBOL_1 else 'ERROR'

        result = self.environment.stake_coin(PAIR_ID, AMOUNT_0, AMOUNT_1)

        self.mock_pool_api.get_pair.assert_called_once_with(PAIR_ID)
        self.mock_portfolio.get_quantity_coin.assert_has_calls([call(SYMBOL_0), call(SYMBOL_1)])
        self.mock_portfolio.stake_coin.assert_called_once_with(PAIR_ID, SYMBOL_0, SYMBOL_1, AMOUNT_0, AMOUNT_1, NO_SUPPLY_TOKENS)
        self.assertTrue(result)

    def test_stake_coin_returns_false_when_liquidity_is_zero(self):
        
        self.mock_pool_api.get_pair.return_value = PAIR
        self.mock_portfolio.get_quantity_coin.side_effect = lambda x: AMOUNT_0 if x == SYMBOL_0 else AMOUNT_1 if x == SYMBOL_1 else 'ERROR'

        result = self.environment.stake_coin(PAIR_ID, 0, 0)

        self.mock_pool_api.get_pair.assert_called_once_with(PAIR_ID)
        self.mock_portfolio.stake_coin.assert_not_called()
        self.assertFalse(result)

    def test_stake_coin_returns_false_when_first_balance_is_zero(self):
        
        self.mock_pool_api.get_pair.return_value = PAIR
        self.mock_portfolio.get_quantity_coin.side_effect = lambda x: 0 if x == SYMBOL_0 else AMOUNT_1 if x == SYMBOL_1 else 'ERROR'

        result = self.environment.stake_coin(PAIR_ID, AMOUNT_0, AMOUNT_1)

        self.mock_portfolio.get_quantity_coin.assert_has_calls([call(SYMBOL_0)])
        self.mock_pool_api.get_pair.assert_called_once_with(PAIR_ID)
        self.mock_portfolio.stake_coin.assert_not_called()
        self.assertFalse(result)

    def test_stake_coin_returns_false_when_second_balance_is_zero(self):
        
        self.mock_pool_api.get_pair.return_value = PAIR
        self.mock_portfolio.get_quantity_coin.side_effect = lambda x: AMOUNT_0 if x == SYMBOL_0 else 0 if x == SYMBOL_1 else 'ERROR'

        result = self.environment.stake_coin(PAIR_ID, AMOUNT_0, AMOUNT_1)

        self.mock_portfolio.get_quantity_coin.assert_has_calls([call(SYMBOL_1)])
        self.mock_pool_api.get_pair.assert_called_once_with(PAIR_ID)
        self.mock_portfolio.stake_coin.assert_not_called()
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
