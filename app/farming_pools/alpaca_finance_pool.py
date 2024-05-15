import os
import requests
from dotenv import load_dotenv

from .farming_pool import IFarmingPool
from .pool import Pool


load_dotenv()

URL = os.getenv('ALPACA_FINANCE_URL')

DATA = 'data'
FARMING_POOLS = 'farmingPools'
SOURCE_NAME = 'sourceName'
TRADING_FEE_APR = 'tradingFeeApr'
BORROWING_INTERESTS = 'borrowingInterests'
INTEREST_PERCENT = 'interestPercent'


class AlpacaFinancePool(IFarmingPool):
    
    def __init__(self) -> None:
        pass
    
    def get_pools(self) -> list[Pool]:
        response = requests.get(URL).json()
        pools = response[DATA][FARMING_POOLS]

        results = []
        for pool in pools:
            
            if len(pool[BORROWING_INTERESTS]) < 2:
                continue
            
            source_name = pool[SOURCE_NAME]
            trading_fee = pool[TRADING_FEE_APR]
            borrow_rate_one = pool[BORROWING_INTERESTS][0][INTEREST_PERCENT]
            borrow_rate_two = pool[BORROWING_INTERESTS][1][INTEREST_PERCENT]
            results.append(Pool(source_name, trading_fee, borrow_rate_one, borrow_rate_two))
        
        return results
