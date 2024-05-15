from app import app
from app.farming_pools.alpaca_finance_pool import AlpacaFinancePool
from app.routes import Routes


if __name__ == '__main__':
    
    farming_pool = AlpacaFinancePool()
    routes = Routes(farming_pool)

    app.run(host="0.0.0.0", debug=True)
