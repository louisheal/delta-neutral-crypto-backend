from flask import Flask
from flask_cors import CORS

from .farming_pools.alpaca_finance_api import AlpacaFinanceApi
from .coin_apis.live_coin_watch_api import LiveCoinWatchApi
from .routes import Routes

from .config import (
  FRONTEND_URL,
  ALPACA_FINANCE_URL,
  COIN_API_KEY,
  COIN_API_URL,  
)

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": [FRONTEND_URL]}})

farming_pool = AlpacaFinanceApi(ALPACA_FINANCE_URL)
coin_api = LiveCoinWatchApi(COIN_API_URL, COIN_API_KEY)

routes = Routes(farming_pool, coin_api)
