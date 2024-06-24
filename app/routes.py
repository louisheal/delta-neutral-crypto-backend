from flask import jsonify, request

from app import app
from app.farming_pools.farming_pool import IFarmingPool
from app.coin_apis.coin_api import ICoinApi
from app.simulation.utils import simulate_position


POOL_ID = 'pool_id'
USD_TO_INVEST = 'usd_to_invest'
DURATION_DAYS = 'duration_days'

GET = 'GET'
POST = 'POST'


class Routes():
    
    def __init__(self, farming_pool: IFarmingPool, coin_api: ICoinApi) -> None:
        self.farming_pool = farming_pool
        self.coin_api = coin_api
        self.__register_routes()
    
    def get_pools(self):
        return jsonify(self.farming_pool.get_pools())
    
    def simulate(self):
        data = request.json

        pool_id = data[POOL_ID]
        duration_days = data[DURATION_DAYS]

        pool = self.farming_pool.get_pool_by_id(pool_id)

        trading_fee = pool.trading_fee
        borrow_rate_one = pool.borrow_rate_one
        borrow_rate_two = pool.borrow_rate_two

        result = simulate_position(duration_days, trading_fee, borrow_rate_one, borrow_rate_two)
        
        return jsonify(result)

    def __register_routes(self):
        app.add_url_rule('/pools', 'get_pools', self.get_pools, methods=[GET])
        app.add_url_rule('/simulate', 'simulate', self.simulate, methods=[POST])
