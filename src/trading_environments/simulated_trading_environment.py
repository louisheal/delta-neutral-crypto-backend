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

        if self.portfolio.get_quantity_dai() < quantity_usd:
            return False
        
        quantity_coin = quantity_usd / self.get_price(coin_symbol)
        return self.portfolio.buy_coin(coin_symbol, quantity_usd, quantity_coin)
    
    def sell_coin(self, coin_symbol: str, quantity_coin: float) -> bool:
        
        if self.portfolio.get_quantity_coin(coin_symbol) < quantity_coin:
            return False

        quantity_usd = quantity_coin * self.get_price(coin_symbol)
        return self.portfolio.sell_coin(coin_symbol, quantity_usd, quantity_coin)

    def stake_coin(self, pair_id: str, quantity_one: float, quantity_two: float) -> bool:
        # TODO: After implementing new number type
        # MINIMUM_LIQUIDITY = 10**3

        pair = self.pool_api.get_pair(pair_id)
        total_supply = pair.total_supply
        reserve_one = pair.reserve0
        reserve_two = pair.reserve1
        symbol_one = pair.symbol0
        symbol_two = pair.symbol1
        
        if total_supply == 0:
            liquidity = math.sqrt(quantity_one * quantity_two) # - MINIMUM_LIQUIDITY
        else:
            liquidity = min((quantity_one * total_supply) / reserve_one,
                            (quantity_two * total_supply) / reserve_two)
        
        balance_one = self.portfolio.get_quantity_coin(symbol_one)
        balance_two = self.portfolio.get_quantity_coin(symbol_two)
        if balance_one < quantity_one or balance_two < quantity_two or liquidity <= 0:
            return False
        
        return self.portfolio.stake_coin(pair_id, symbol_one, symbol_two, quantity_one, quantity_two, liquidity)
    
    def unstake_coin(self, pair_id: str, quantity_lp_tokens: float) -> bool:

        lp_balance = self.portfolio.get_quantity_coin(pair_id)
        if lp_balance < quantity_lp_tokens:
            return False
        
        pair = self.pool_api.get_pair(pair_id)
        total_supply = pair.total_supply
        reserve_one = pair.reserve0
        reserve_two = pair.reserve1
        symbol_one = pair.symbol0
        symbol_two = pair.symbol1
        
        quantity_one = (quantity_lp_tokens / total_supply) * reserve_one
        quantity_two = (quantity_lp_tokens / total_supply) * reserve_two

        return self.portfolio.unstake_coin(pair_id, symbol_one, symbol_two, quantity_one, quantity_two, quantity_lp_tokens)
