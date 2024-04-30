import json
import requests

from .coin_api_adapter import ICoinApiAdapter


class LiveCoinWatchAdapter(ICoinApiAdapter):
    
    def __init__(self, base_url, api_key) -> None:
        self.base_url = base_url
        self.api_key = api_key

    def get_price(self, ticker: str) -> float:
        payload = json.dumps({
            'currency': 'USD',
            'code': ticker,
            'meta': False
        })
        headers = {
            'content-type': 'application/json',
            'x-api-key': self.api_key
        }
        response = requests.post(f"{self.base_url}/coins/single", headers=headers, data=payload)
        data = response.json()
        return data['rate']
