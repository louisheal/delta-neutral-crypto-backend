import matplotlib.pyplot as plt
import unittest

from src.simulation.simulation_utils import simulate_position


AMOUNT_TO_INVEST = 200
DURATION_DAYS = 360
DURATION_YEARS = DURATION_DAYS / 365
PRICE_TOKEN_ONE = 1
PRICE_TOKEN_TWO = 24
TRADING_FEES = 0.5295
BORROW_RATE_ONE = 0.18
BORROW_RATE_TWO = 0.21


class TestSimulationUtils(unittest.TestCase):
    
    def test_simulate_position(self):
        
        x, long, short, total = simulate_position(AMOUNT_TO_INVEST, DURATION_YEARS, PRICE_TOKEN_ONE,
                                                  PRICE_TOKEN_TWO, TRADING_FEES, BORROW_RATE_ONE, BORROW_RATE_TWO)
        
        plt.plot(x, long, lw=1, label="Long")
        plt.plot(x, short, lw=1, label="Short")
        plt.plot(x, total, lw=2, label="Combined")
        plt.title(f"Profit after {DURATION_DAYS} days with {TRADING_FEES * 100}% APR")
        plt.ylabel("Profits in USD")
        plt.xlabel("Price of Token 2 in USD")
        plt.legend()
        plt.grid()
        plt.show()
