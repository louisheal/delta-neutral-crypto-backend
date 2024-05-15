from app import app
from app.farming_pools.alpaca_finance_pool import AlpacaFinancePool
from app.routes import Routes


farming_pool = AlpacaFinancePool()
routes = Routes(farming_pool)

if __name__ == '__main__':
    app.run(host="localhost", debug=True)
