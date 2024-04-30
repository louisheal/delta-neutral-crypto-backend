import json
import requests

from .trading_environment import ITradingEnvironment


class SimulatedTradingEnvironment(ITradingEnvironment):
    
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
    
    def get_price(self, symbol: str) -> float:
        payload = json.dumps({
            'currency': 'USD',
            'code': symbol,
            'meta': False
        })
        headers = {
            'content-type': 'application/json',
            'x-api-key': self.api_key
        }
        response = requests.post(f"{self.base_url}/coins/single", headers=headers, data=payload)
        data = response.json()
        return data['rate']
