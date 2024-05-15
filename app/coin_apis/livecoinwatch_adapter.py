import json
import requests

from .coin_api import ICoinApi


CODE = 'code'
RATE = 'rate'

CONTENT_TYPE = 'content-type'
APPLICATION_JSON = 'application/json'
X_API_KEY = 'x-api-key'


class LiveCoinWatchAdapter(ICoinApi):
    
    def __init__(self, base_url, api_key) -> None:
        self.base_url = base_url
        self.api_key = api_key

    def get_price_by_symbol(self, symbol: str) -> float:
        payload = json.dumps({ CODE: symbol })
        headers = {
            CONTENT_TYPE: APPLICATION_JSON,
            X_API_KEY: self.api_key
        }
        response = requests.post(f"{self.base_url}/coins/single", headers=headers, data=payload)
        data = response.json()
        return data[RATE]
