from flask import jsonify

from app import app
from app.simulation.simulation_utils import simulate_position


FARM_POOL_API = 'FARM_POOL_API'

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/pools')
def get_pools():
    farm_pool_api = app.config[FARM_POOL_API]
    pools = farm_pool_api.get_pools()
    return jsonify(pools)

@app.route('/simulateTrade')
def simulate_trade():
    return simulate_position()
