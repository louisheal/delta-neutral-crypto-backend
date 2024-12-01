import os
from dotenv import load_dotenv

load_dotenv()

def get_secret(secret_name):
    secret_path = f"/run/secrets/{secret_name}"
    if os.path.exists(secret_path):
        with open(secret_path, 'r') as f:
            return f.read().strip()
    return os.getenv(secret_name)

FRONTEND_URL = get_secret('DN_FRONTEND_URL')
ALPACA_FINANCE_URL = "https://alpaca-static-api.alpacafinance.org/bsc/v1/landing/summary.json"
