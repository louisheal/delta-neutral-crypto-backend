from flask import jsonify

from app import app
from app.farming_pools.farming_pool import IFarmingPool
from app.simulation.simulation_utils import simulate_position


class Routes():
    
    def __init__(self, farming_pool: IFarmingPool) -> None:
        self.farming_pool = farming_pool
        self.__register_routes()

    def index(self):
        return 'Hello World!'
    
    def get_pools(self):
        return jsonify(self.farming_pool.get_pools())
    
    def simulate_trade(self):
        return jsonify(simulate_position())

    def __register_routes(self):
        app.add_url_rule('/', 'index', self.index)
        app.add_url_rule('/pools', 'get_pools', self.get_pools)
        app.add_url_rule('/simulatePosition', 'simulate_position', self.simulate_trade)
