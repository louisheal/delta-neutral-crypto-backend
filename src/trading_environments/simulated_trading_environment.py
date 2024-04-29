import requests
import os
from dotenv import load_dotenv

from .trading_environment import ITradingEnvironment


load_dotenv()
API_KEY = os.getenv('API_KEY')

class SimulatedTradingEnvironment(ITradingEnvironment):
    
    def __init__(self, base_url: str):
        self.base_url = base_url
    
    def get_price(self, symbol: str) -> float:
        payload = {'currency':'USD', 'code':symbol}
        headers = {
            'content-type': 'application/json',
            'x-api-key': API_KEY
        }
        response = requests.post(self.base_url, headers=headers, data=payload)
        data = response.json()
        return data['rate']
