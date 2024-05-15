import os
from dotenv import load_dotenv

from app import app
from app.farming_pools.alpaca_finance_pool import AlpacaFinancePool
from app.coin_apis.livecoinwatch_adapter import LiveCoinWatchAdapter
from app.routes import Routes


load_dotenv()

ALPACA_FINANCE_URL = os.getenv('ALPACA_FINANCE_URL')
COIN_API_URL = os.getenv('COIN_API_URL')
COIN_API_KEY = os.getenv('COIN_API_KEY')

farming_pool = AlpacaFinancePool(ALPACA_FINANCE_URL)
coin_api = LiveCoinWatchAdapter(COIN_API_URL, COIN_API_KEY)

routes = Routes(farming_pool, coin_api)

if __name__ == '__main__':
    app.run(host="localhost", debug=True)
