from app.farming_pools.farming_pool import IFarmingPool
from app.farming_pools.pool import Pool


USDT_BNB = 'usdt_bnb'
USDT_BNB_POOL = Pool(USDT_BNB, 'USDT BNB', 'BNB', 'USDT', 0.21, 0.08, 0.11)
POOLS = [USDT_BNB_POOL]


class TestFarmingPool(IFarmingPool):
  
  def get_pools(self) -> list[Pool]:
    return POOLS
  
  def get_pool_by_id(self, pool_id: str) -> Pool:
    if pool_id == USDT_BNB:
      return USDT_BNB_POOL
    return None
