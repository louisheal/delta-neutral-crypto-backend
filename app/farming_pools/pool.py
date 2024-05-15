from dataclasses import dataclass


@dataclass
class Pool:
    id: str
    pool_name: str
    token_one_symbol: str
    token_two_symbol: str
    trading_fee: float
    borrow_rate_one: float
    borrow_rate_two: float
