import os
from dotenv import load_dotenv
from flask_cors import CORS

from app import app
from app.farming_pools.alpaca_finance_api import AlpacaFinanceApi
from app.coin_apis.live_coin_watch_api import LiveCoinWatchApi
from app.routes import Routes


load_dotenv()

FRONTEND_URL = os.getenv('FRONTEND_URL')
ALPACA_FINANCE_URL = os.getenv('ALPACA_FINANCE_URL')
COIN_API_URL = os.getenv('COIN_API_URL')
COIN_API_KEY = os.getenv('COIN_API_KEY')

CORS(app, resources={r"/pools": {"origins": [FRONTEND_URL]}})

farming_pool = AlpacaFinanceApi(ALPACA_FINANCE_URL)
coin_api = LiveCoinWatchApi(COIN_API_URL, COIN_API_KEY)

routes = Routes(farming_pool, coin_api)

if __name__ == '__main__':
    app.run(debug=True)
