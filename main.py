from app import app
from app.farming_pools.alpaca_finance_pool import AlpacaFinancePool


FARM_POOL_API = 'FARM_POOL_API'


if __name__ == '__main__':
    app.config[FARM_POOL_API] = AlpacaFinancePool()
    app.run(host="0.0.0.0", debug=True)
