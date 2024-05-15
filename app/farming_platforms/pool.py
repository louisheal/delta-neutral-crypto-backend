from dataclasses import dataclass


@dataclass
class Pool:
    pool_name: str
    trading_fee: float
    borrow_rate_one: float
    borrow_rate_two: float
