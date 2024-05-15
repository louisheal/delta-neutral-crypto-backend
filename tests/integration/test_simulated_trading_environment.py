import os
import unittest
from dotenv import load_dotenv
from pathlib import Path

from app.coin_api_adapters.livecoinwatch_adapter import LiveCoinWatchAdapter
from app.liquidity_pool_apis.uniswap_api import UniswapApi
from app.portfolios.csv_portfolio import CsvPortfolio
from app.trading_environments.simulated_trading_environment import SimulatedTradingEnvironment

from tests.integration.utils import save_csv_portfolio


load_dotenv()

COIN_URL = os.getenv('COIN_URL')
COIN_API_KEY = os.getenv('COIN_API_KEY')

GRAPH_URL = os.getenv('GRAPH_URL')
GRAPH_API_KEY = os.getenv('GRAPH_API_KEY')
UNISWAP_APP_ID = os.getenv('UNISWAP_APP_ID')

PORTFOLIO_PATH = Path('tests/integration/fixtures/test_portfolio.csv')

PAIR_ID = "0xa478c2975ab1ea89e8196811f51a7b7ade33eb11"

DAI = 'DAI'
WETH = 'WETH'

ZERO = 0.0
QUANTITY_DAI = 500
QUANTITY_WETH = 1
QUANTITY_LP_TOKENS = 10


class TestSimulatedTradingEnvironment(unittest.TestCase):

    def setUp(self):
       self.coin_api = LiveCoinWatchAdapter(COIN_URL, COIN_API_KEY)
       self.pool_api = UniswapApi(GRAPH_URL, GRAPH_API_KEY, UNISWAP_APP_ID)
       self.portfolio = CsvPortfolio(PORTFOLIO_PATH)
       self.environment = SimulatedTradingEnvironment(self.coin_api, self.pool_api, self.portfolio)
    
    def test_get_price_returns(self):
        price = self.environment.get_price(WETH)
        self.assertIsNotNone(price)

    def test_buy_coin_adds_to_portfoilio(self):
        self.__setup_buy_coin_tests()

        result = self.environment.buy_coin(WETH, QUANTITY_DAI)
        quantity_dai = self.portfolio.get_quantity_dai()
        quantity_weth = self.portfolio.get_quantity_coin(WETH)
        
        self.assertEqual(quantity_dai, ZERO)
        self.assertGreater(quantity_weth, ZERO)
        self.assertTrue(result)
    
    def test_buy_coin_fails_when_not_enough_funds(self):
        self.__setup_buy_coin_tests()

        result = self.environment.buy_coin(WETH, QUANTITY_DAI + 1)
        quantity_dai = self.portfolio.get_quantity_dai()
        quantity_weth = self.portfolio.get_quantity_coin(WETH)
        
        self.assertEqual(quantity_dai, QUANTITY_DAI)
        self.assertEqual(quantity_weth, ZERO)
        self.assertFalse(result)
    
    def test_sell_coin_removes_from_portfolio(self):
        self.__setup_sell_coin_tests()

        result = self.environment.sell_coin(WETH, QUANTITY_WETH)
        quantity_dai = self.portfolio.get_quantity_dai()
        quantity_weth = self.portfolio.get_quantity_coin(WETH)
        
        self.assertEqual(quantity_weth, ZERO)
        self.assertGreater(quantity_dai, ZERO)
        self.assertTrue(result)

    def test_sell_coin_fails_when_not_enough_funds(self):
        self.__setup_sell_coin_tests()

        result = self.environment.sell_coin(WETH, QUANTITY_WETH + 1)
        quantity_dai = self.portfolio.get_quantity_dai()
        quantity_weth = self.portfolio.get_quantity_coin(WETH)
        
        self.assertEqual(quantity_dai, ZERO)
        self.assertEqual(quantity_weth, QUANTITY_WETH)
        self.assertFalse(result)

    def test_stake_coin_adds_lp_tokens_to_portfolio(self):
        self.__setup_stake_coin_tests()

        result = self.environment.stake_coin(PAIR_ID, QUANTITY_DAI, QUANTITY_WETH)
        quantity_dai = self.portfolio.get_quantity_dai()
        quantity_weth = self.portfolio.get_quantity_coin(WETH)
        quantity_lp_tokens = self.portfolio.get_quantity_coin(PAIR_ID)

        self.assertEqual(quantity_dai, ZERO)
        self.assertEqual(quantity_weth, ZERO)
        self.assertGreater(quantity_lp_tokens, ZERO)
        self.assertTrue(result)

    def test_unstake_coin_removes_lp_tokens_from_portfolio(self):
        self.__setup_unstake_coin_tests()

        result = self.environment.unstake_coin(PAIR_ID, QUANTITY_LP_TOKENS)
        quantity_dai = self.portfolio.get_quantity_dai()
        quantity_weth = self.portfolio.get_quantity_coin(WETH)
        quantity_lp_tokens = self.portfolio.get_quantity_coin(PAIR_ID)

        self.assertGreater(quantity_dai, ZERO)
        self.assertGreater(quantity_weth, ZERO)
        self.assertEqual(quantity_lp_tokens, ZERO)
        self.assertTrue(result)
    
    def __setup_buy_coin_tests(self):
        portfolio = {
            DAI: QUANTITY_DAI
        }
        save_csv_portfolio(portfolio, PORTFOLIO_PATH)
    
    def __setup_sell_coin_tests(self):
        portfolio = {
            WETH: QUANTITY_WETH
        }
        save_csv_portfolio(portfolio, PORTFOLIO_PATH)

    def __setup_stake_coin_tests(self):
        portfolio = {
            DAI: QUANTITY_DAI,
            WETH: QUANTITY_WETH
        }
        save_csv_portfolio(portfolio, PORTFOLIO_PATH)

    def __setup_unstake_coin_tests(self):
        portfolio = {
            PAIR_ID: QUANTITY_LP_TOKENS
        }
        save_csv_portfolio(portfolio, PORTFOLIO_PATH)


if __name__ == '__main__':
    unittest.main()
