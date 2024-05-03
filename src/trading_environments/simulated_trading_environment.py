import math

from ..coin_api_adapters.coin_api_adapter import ICoinApiAdapter
from .trading_environment import ITradingEnvironment
from ..portfolios.portfolio import IPortfolio


class SimulatedTradingEnvironment(ITradingEnvironment):
    
    def __init__(self, coin_api: ICoinApiAdapter, portfolio: IPortfolio):
        self.coin_api = coin_api
        self.portfolio = portfolio
    
    def get_price(self, coin_symbol: str) -> float:
        return self.coin_api.get_price(coin_symbol)
    
    def buy_coin(self, coin_symbol: str, quantity_usd: float) -> bool:

        if self.portfolio.get_quantity_usd() < quantity_usd:
            return False
        
        quantity_coin = quantity_usd / self.get_price(coin_symbol)
        return self.portfolio.buy_coin(coin_symbol, quantity_usd, quantity_coin)
    
    def sell_coin(self, coin_symbol: str, quantity_coin: float) -> bool:
        
        if self.portfolio.get_quantity_coin(coin_symbol) < quantity_coin:
            return False

        quantity_usd = quantity_coin * self.get_price(coin_symbol)
        return self.portfolio.sell_coin(coin_symbol, quantity_usd, quantity_coin)
    
    def stake_coin(self, pool_id: str, amount0: float, amount1: float) -> bool:
        # TODO: After using new number type
        # MINIMUM_LIQUIDITY = 10**3

        # TODO: Find total_supply, reserve0, reserve1, symbol0 and symbol1 of pool_id
        total_supply = 0
        reserve0 = 0
        reserve1 = 0
        symbol0 = 'ETH'
        symbol1 = 'USD'

        balance0 = self.portfolio.get_quantity_coin(symbol0)
        balance1 = self.portfolio.get_quantity_coin(symbol1)
        if balance0 < amount0 or balance1 < amount1:
            return False
        
        # TODO: Check that both sides of the stake are equal (or close enough)
        
        if total_supply == 0:
            liquidity = math.sqrt(amount0 * amount1)
        else:
            liquidity = min((amount0 * total_supply) / reserve0,
                            (amount1 * total_supply) / reserve1)
        # TODO: Better check: liquidity needs to be greater than 0
        assert liquidity > 0

        # TODO: Store liquidity tokens owned for this pool in csv
