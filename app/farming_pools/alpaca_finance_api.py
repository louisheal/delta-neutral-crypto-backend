import math
import requests

from .farming_pool import IFarmingPool
from .pool import Pool
from app.simulation.utils import calculate_apy


DATA = 'data'
FARMING_POOLS = 'farmingPools'

KEY = 'key'
SOURCE_NAME = 'sourceName'
TRADING_FEE_APR = 'tradingFeeApr'
BORROWING_INTERESTS = 'borrowingInterests'
INTEREST_PERCENT = 'interestPercent'
WORKING_TOKEN = 'workingToken'
TOKEN_A = 'tokenA'
TOKEN_B = 'tokenB'
SYMBOL = 'symbol'


class AlpacaFinanceApi(IFarmingPool):
    
    def __init__(self, base_url) -> None:
        self.base_url = base_url
    
    def get_pools(self) -> list[Pool]:
        response = requests.get(self.base_url).json()
        pools = response[DATA][FARMING_POOLS]

        results = []
        for pool in pools:
            
            if len(pool[BORROWING_INTERESTS]) < 2:
                continue
            
            borrow_rate_one = float(pool[BORROWING_INTERESTS][0][INTEREST_PERCENT]) / 200
            borrow_rate_two = float(pool[BORROWING_INTERESTS][1][INTEREST_PERCENT]) / 200

            if borrow_rate_one == 0.0 or borrow_rate_two == 0.0:
                continue
            
            pool_id = pool[KEY]
            pool_name = pool[SOURCE_NAME]
            trading_fee = float(pool[TRADING_FEE_APR]) / 300
            token_one_symbol = pool[WORKING_TOKEN][TOKEN_A][SYMBOL]
            token_two_symbol = pool[WORKING_TOKEN][TOKEN_B][SYMBOL]

            # TODO: Check order of borrow rates
            trading_fee_interest = math.exp(trading_fee)
            stablecoin_interest = math.exp(borrow_rate_one)
            non_stable_interest = math.exp(borrow_rate_two)
            apy = calculate_apy(trading_fee_interest, stablecoin_interest, non_stable_interest, 3, 1)

            results.append(Pool(pool_id, pool_name, token_one_symbol, token_two_symbol, trading_fee, borrow_rate_one, borrow_rate_two, apy))
        
        return results

    def get_pool_by_id(self, pool_id: str) -> Pool:
        response = requests.get(self.base_url).json()
        pools = response[DATA][FARMING_POOLS]

        for pool in pools:
            
            if pool[KEY] == pool_id:
                source_name = pool[SOURCE_NAME]
                trading_fee = float(pool[TRADING_FEE_APR]) / 300
                token_one_symbol = pool[WORKING_TOKEN][TOKEN_A][SYMBOL]
                token_two_symbol = pool[WORKING_TOKEN][TOKEN_B][SYMBOL]
                borrow_rate_one = float(pool[BORROWING_INTERESTS][0][INTEREST_PERCENT]) / 200
                borrow_rate_two = float(pool[BORROWING_INTERESTS][1][INTEREST_PERCENT]) / 200

                return Pool(pool_id, source_name, token_one_symbol, token_two_symbol, trading_fee, borrow_rate_one, borrow_rate_two, 0)
        
        return None
    