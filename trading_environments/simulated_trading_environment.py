from trading_environment import ITradingEnvironment


# TODO: STE needs to take inputs (api url for example)
class SimulatedTradingEnvironment(ITradingEnvironment):
    
    def get_price(self, symbol: str) -> float:
        pass
