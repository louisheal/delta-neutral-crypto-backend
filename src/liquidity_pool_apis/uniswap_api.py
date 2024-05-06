import requests

from .liquidity_pool_api import ILiquidityPoolApi
from .pair import Pair


DATA = 'data'
PAIR = 'pair'
ID = 'id'
TOTAL_SUPPLY = 'totalSupply'
RESERVE_0 = 'reserve0'
RESERVE_1 = 'reserve1'
TOKEN_0 = 'token0'
TOKEN_1 = 'token1'
SYMBOL = 'symbol'


class UniswapApi(ILiquidityPoolApi):
    
    def __init__(self, url: str, api_key: str, app_id: str) -> None:
        self.url = url
        self.api_key = api_key
        self.app_id = app_id

    def get_pair(self, pair_id: str) -> Pair:
        query = self.__query_pair_by_id(pair_id)

        response = requests.post(f"{self.url}/api/{self.api_key}/subgraphs/id/{self.app_id}", json={'query': query})
        data = response.json()[DATA][PAIR]

        return self.__data_to_pair(data)
    
    def __data_to_pair(self, data: str) -> Pair:
        return Pair(data[ID],
                    float(data[TOTAL_SUPPLY]),
                    float(data[RESERVE_0]),
                    float(data[RESERVE_1]),
                    data[TOKEN_0][SYMBOL],
                    data[TOKEN_1][SYMBOL])
    
    def __query_pair_by_id(self, pair_id: str):
        return f"""
        {{
            pair(id: "{pair_id}") {{
                id
                totalSupply
                reserve0
                reserve1
                token0 {{
                    symbol
                }}
                token1 {{
                    symbol
                }}
            }}
        }}
        """
