from flask import jsonify, current_app

from app import app
from app.simulation.simulation_utils import simulate_position


FARM_POOL_API = 'FARM_POOL_API'

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/pools')
def get_pools():
    farm_pool_api = current_app.config[FARM_POOL_API]
    pools = farm_pool_api.get_pools()
    return jsonify(pools)

# TODO: Take in vars (from url? from posted json request)
@app.route('/simulateTrade')
def simulate_trade():
    
    # usd_to_invest : from frontend
    # duration_years : from frontend
    # price_one_usd : from coin_api / farm_pool_api
    # price_two_usd : from coin_api / farm_pool_api
    # trading_fees : from farm_pool_api
    # borrow_rate_one : from farm_pool_api
    # borrow_rate_one : from farm_pool_api

    ## farming_pool_id : from frontend (user selects pool to simulate)

    return jsonify(simulate_position())
