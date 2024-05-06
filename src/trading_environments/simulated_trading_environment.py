import math

from .trading_environment import ITradingEnvironment
from ..coin_api_adapters.coin_api_adapter import ICoinApiAdapter
from ..liquidity_pool_apis.liquidity_pool_api import ILiquidityPoolApi
from ..portfolios.portfolio import IPortfolio


class SimulatedTradingEnvironment(ITradingEnvironment):
    
    def __init__(self, coin_api: ICoinApiAdapter, pool_api: ILiquidityPoolApi, portfolio: IPortfolio):
        self.coin_api = coin_api
        self.pool_api = pool_api
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

    def stake_coin(self, pair_id: str, amount_0: float, amount_1: float) -> bool:
        # TODO: After implementing new number type
        # MINIMUM_LIQUIDITY = 10**3

        pair = self.pool_api.get_pair(pair_id)
        total_supply = pair.total_supply
        reserve_0 = pair.reserve0
        reserve_1 = pair.reserve1
        symbol_0 = pair.symbol0
        symbol_1 = pair.symbol1
        
        if total_supply == 0:
            liquidity = math.sqrt(amount_0 * amount_1) # - MINIMUM_LIQUIDITY
        else:
            liquidity = min((amount_0 * total_supply) / reserve_0,
                            (amount_1 * total_supply) / reserve_1)
        
        balance_0 = self.portfolio.get_quantity_coin(symbol_0)
        balance_1 = self.portfolio.get_quantity_coin(symbol_1)
        if balance_0 < amount_0 or balance_1 < amount_1 or liquidity <= 0:
            return False
        
        return self.portfolio.stake_coin(pair_id, symbol_0, symbol_1, amount_0, amount_1, liquidity)
