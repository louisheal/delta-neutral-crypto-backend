import unittest
from unittest.mock import MagicMock, call

from src.coin_api_adapters.coin_api_adapter import ICoinApiAdapter
from src.liquidity_pool_apis.pair import Pair
from src.liquidity_pool_apis.liquidity_pool_api import ILiquidityPoolApi
from src.portfolios.portfolio import IPortfolio
from src.trading_environments.simulated_trading_environment import SimulatedTradingEnvironment


PRICE = 50.0

ZERO = 0.0

QUANTITY_DAI = 1000
QUANTITY_WETH = 10
QUANTITY_LP_TOKENS = 20
QUANTITY_LP_TOKENS_NO_SUPPLY = 100

PAIR_ID = 'PAIR_ID'
TOTAL_SUPPLY = 100
RESERVE_0 = 5000
RESERVE_1 = 50

DAI = 'DAI'
WETH = 'WETH'

PAIR = Pair(PAIR_ID, TOTAL_SUPPLY, RESERVE_0, RESERVE_1, DAI, WETH)
PAIR_NO_SUPPLY = Pair(PAIR_ID, ZERO, RESERVE_0, RESERVE_1, DAI, WETH)


class TestSimulatedTradingEnvironment(unittest.TestCase):
    
    def setUp(self) -> None:
        self.mock_coin_api = MagicMock(spec=ICoinApiAdapter)
        self.mock_pool_api = MagicMock(spec=ILiquidityPoolApi)
        self.mock_portfolio = MagicMock(spec=IPortfolio)
        self.environment = SimulatedTradingEnvironment(self.mock_coin_api, self.mock_pool_api, self.mock_portfolio)
    
    def test_get_price_returns_correct_value(self):

        self.mock_coin_api.get_price.return_value = PRICE

        price = self.environment.get_price(WETH)

        self.mock_coin_api.get_price.assert_called_once_with(WETH)
        self.assertEqual(price, PRICE)

    def test_buy_coin_calls_portfolio_with_correct_values(self):
        
        self.mock_coin_api.get_price.return_value = PRICE
        self.mock_portfolio.get_quantity_dai.return_value = QUANTITY_DAI
        self.mock_portfolio.buy_coin.return_value = True

        result = self.environment.buy_coin(WETH, QUANTITY_DAI)
        
        self.mock_coin_api.get_price.assert_called_once_with(WETH)
        self.mock_portfolio.get_quantity_dai.assert_called_once()
        self.mock_portfolio.buy_coin.assert_called_once_with(WETH, QUANTITY_DAI, QUANTITY_DAI / PRICE)
        self.assertTrue(result)
    
    def test_buy_coin_returns_false_when_insufficient_funds(self):
        
        self.mock_portfolio.get_quantity_dai.return_value = ZERO
        
        result = self.environment.buy_coin(WETH, QUANTITY_DAI)
        
        self.mock_portfolio.get_quantity_dai.assert_called_once()
        self.assertFalse(result)
    
    def test_sell_coin_calls_portfolio_with_correct_values(self):
        
        self.mock_coin_api.get_price.return_value = PRICE
        self.mock_portfolio.get_quantity_coin.return_value = QUANTITY_DAI / PRICE
        self.mock_portfolio.sell_coin.return_value = True

        result = self.environment.sell_coin(WETH, QUANTITY_DAI / PRICE)
        
        self.mock_coin_api.get_price.assert_called_once_with(WETH)
        self.mock_portfolio.get_quantity_coin.assert_called_once_with(WETH)
        self.mock_portfolio.sell_coin.assert_called_once_with(WETH, QUANTITY_DAI, QUANTITY_DAI / PRICE)
        self.assertTrue(result)
    
    def test_sell_coin_returns_false_when_insufficient_funds(self):
        
        self.mock_portfolio.get_quantity_coin.return_value = ZERO

        result = self.environment.sell_coin(WETH, QUANTITY_DAI)
        
        self.mock_portfolio.get_quantity_coin.assert_called_once_with(WETH)
        self.assertFalse(result)

    def test_stake_coin_calculates_lp_tokens_when_supply_greater_than_zero(self):
        
        self.mock_pool_api.get_pair.return_value = PAIR
        self.mock_portfolio.get_quantity_coin.side_effect = self.__quantity_coin_side_effect(QUANTITY_DAI, QUANTITY_WETH, DAI, WETH)

        result = self.environment.stake_coin(PAIR_ID, QUANTITY_DAI, QUANTITY_WETH)

        self.mock_pool_api.get_pair.assert_called_once_with(PAIR_ID)
        self.mock_portfolio.get_quantity_coin.assert_has_calls([call(DAI), call(WETH)])
        self.mock_portfolio.stake_coin.assert_called_once_with(PAIR_ID, DAI, WETH, QUANTITY_DAI, QUANTITY_WETH, QUANTITY_LP_TOKENS)
        self.assertTrue(result)

    def test_stake_coin_calculates_lp_tokens_when_supply_is_zero(self):
        
        self.mock_pool_api.get_pair.return_value = PAIR_NO_SUPPLY
        self.mock_portfolio.get_quantity_coin.side_effect = self.__quantity_coin_side_effect(QUANTITY_DAI, QUANTITY_WETH, DAI, WETH)

        result = self.environment.stake_coin(PAIR_ID, QUANTITY_DAI, QUANTITY_WETH)

        self.mock_pool_api.get_pair.assert_called_once_with(PAIR_ID)
        self.mock_portfolio.get_quantity_coin.assert_has_calls([call(DAI), call(WETH)])
        self.mock_portfolio.stake_coin.assert_called_once_with(PAIR_ID, DAI, WETH, QUANTITY_DAI, QUANTITY_WETH, QUANTITY_LP_TOKENS_NO_SUPPLY)
        self.assertTrue(result)

    def test_stake_coin_returns_false_when_liquidity_is_zero(self):
        
        self.mock_pool_api.get_pair.return_value = PAIR
        self.mock_portfolio.get_quantity_coin.side_effect = self.__quantity_coin_side_effect(QUANTITY_DAI, QUANTITY_WETH, DAI, WETH)

        result = self.environment.stake_coin(PAIR_ID, ZERO, ZERO)

        self.mock_pool_api.get_pair.assert_called_once_with(PAIR_ID)
        self.mock_portfolio.stake_coin.assert_not_called()
        self.assertFalse(result)

    def test_stake_coin_returns_false_when_first_balance_is_zero(self):
        
        self.mock_pool_api.get_pair.return_value = PAIR
        self.mock_portfolio.get_quantity_coin.side_effect = self.__quantity_coin_side_effect(ZERO, QUANTITY_WETH, DAI, WETH)

        result = self.environment.stake_coin(PAIR_ID, QUANTITY_DAI, QUANTITY_WETH)

        self.mock_portfolio.get_quantity_coin.assert_has_calls([call(DAI)])
        self.mock_pool_api.get_pair.assert_called_once_with(PAIR_ID)
        self.mock_portfolio.stake_coin.assert_not_called()
        self.assertFalse(result)

    def test_stake_coin_returns_false_when_second_balance_is_zero(self):
        
        self.mock_pool_api.get_pair.return_value = PAIR
        self.mock_portfolio.get_quantity_coin.side_effect = self.__quantity_coin_side_effect(QUANTITY_DAI, ZERO, DAI, WETH)

        result = self.environment.stake_coin(PAIR_ID, QUANTITY_DAI, QUANTITY_WETH)

        self.mock_portfolio.get_quantity_coin.assert_has_calls([call(WETH)])
        self.mock_pool_api.get_pair.assert_called_once_with(PAIR_ID)
        self.mock_portfolio.stake_coin.assert_not_called()
        self.assertFalse(result)

    def test_unstake_coin_removes_lp_tokens(self):
        
        self.mock_pool_api.get_pair.return_value = PAIR
        self.mock_portfolio.get_quantity_coin.return_value = QUANTITY_LP_TOKENS

        result = self.environment.unstake_coin(PAIR_ID, QUANTITY_LP_TOKENS)

        self.mock_portfolio.get_quantity_coin.assert_called_once_with(PAIR_ID)
        self.mock_portfolio.unstake_coin.assert_called_once_with(PAIR_ID, DAI, WETH, QUANTITY_DAI, QUANTITY_WETH, QUANTITY_LP_TOKENS)
        self.assertTrue(result)

    def test_unstake_coin_fails_when_not_enough_lp_tokens(self):
        
        self.mock_pool_api.get_pair.return_value = PAIR
        self.mock_portfolio.get_quantity_coin.return_value = ZERO

        result = self.environment.unstake_coin(PAIR_ID, QUANTITY_LP_TOKENS)

        self.mock_portfolio.get_quantity_coin.assert_called_once_with(PAIR_ID)
        self.mock_portfolio.unstake_coin.assert_not_called()
        self.assertFalse(result)

    def __quantity_coin_side_effect(self, amount_0: float, amount_1: float, symbol_0: str, symbol_1: str):
        return lambda x: amount_0 if x == symbol_0 else amount_1 if x == symbol_1 else 'ERROR'


if __name__ == '__main__':
    unittest.main()
