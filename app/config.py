import os
from dotenv import load_dotenv

load_dotenv()

FRONTEND_URL = os.getenv('FRONTEND_URL')
ALPACA_FINANCE_URL = "https://alpaca-static-api.alpacafinance.org/bsc/v1/landing/summary.json"
