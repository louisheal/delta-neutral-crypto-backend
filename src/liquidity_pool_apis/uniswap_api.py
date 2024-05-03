import requests

from .liquidity_pool_api import ILiquidityPoolApi
from .pair import Pair


class UniswapApi(ILiquidityPoolApi):
    
    def __init__(self, url: str, app_id: str, api_key: str) -> None:
        self.url = f"{url}/api/{api_key}/subgraphs/id/{app_id}"

    def get_pair(self, pair_id: str) -> Pair:
        query = self.__query_pair_by_id(pair_id)

        response = requests.post(self.url, json={'query': query})
        data = response.json()

        return self.__data_to_pair(data)
    
    def __data_to_pair(self, data: str) -> Pair:
        return Pair(data['id'],
                    data['totalSupply'],
                    data['reserve0'],
                    data['reserve1'],
                    data['token0']['symbol'],
                    data['token1']['symbol'])
    
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
