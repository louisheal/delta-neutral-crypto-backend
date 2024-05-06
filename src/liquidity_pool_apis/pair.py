from dataclasses import dataclass


@dataclass
class Pair:
    pair_id: str
    total_supply: float
    reserve0: float
    reserve1: float
    symbol0: str
    symbol1: str
