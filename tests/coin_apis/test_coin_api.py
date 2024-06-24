from app.coin_apis.coin_api import ICoinApi


class TestCoinApi(ICoinApi):
  
  def get_price_by_symbol(self, symbol: str) -> float:
    if symbol == 'CAKE':
      return 2.03
    if symbol == 'BNB':
      return 623.11
    if symbol == 'USDT':
      return 1.0
