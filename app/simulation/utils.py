import math


def simulate_position(duration_days: int, trading_fee_rate: float, stablecoin_rate: float,
                      non_stable_rate: float) -> tuple[list[float], list[float]]:
    """
    Returns the values necessary to plot a graph of the value of the long position, short position and total position against the price of the asset.

    :param float duration_days: The amount of time to invest for, in days.
    :param float trading_fee_rate: The average interest earned on invested tokens, as a percentage.
    :param float stablecoin_rate: The interest rate for borrowing stablecoin tokens, as a percentage.
    :param float non_stable_rate: The interest rate for borrowing non-stable tokens, as a percentage.
    """
    
    price_range = [x / 100 for x in range(25, 200, 5)]
    labels = [f"{x - 100}%" for x in range(25, 200, 5)]
    total_profits = []

    trading_fee_interest = math.exp(trading_fee_rate * duration_days / 365)
    stablecoin_interest = math.exp(stablecoin_rate * duration_days / 365)
    non_stable_interest = math.exp(non_stable_rate * duration_days / 365)

    for price_change in price_range:
        total_profits.append(calculate_apy(trading_fee_interest, stablecoin_interest, non_stable_interest, 3, price_change) * 100)

    return labels, total_profits


def calculate_apy(I_1: float, I_2: float, I_3: float, L: float, k) -> float:
    """
    Returns the Return on Investment for a Leveraged Pseudo Delta-Neutral investment.
    (Uses the formula defined in Appendix A.4 of the Pseudo Delta-Neutral Crypto Trading paper).

    :param float I_1: The interest accrued from trading fees
    :param float I_2: The interest accrued from borrowing non-stable tokens
    :param float I_3: The interest accrued from borrowing stablecoin tokens
    :param float L: The leverage used in the position
    :param float k: The change in price of the non-stable token as a percentage
    """
    return ((I_1 + 1) * L * math.sqrt(k) / 2) - (I_2 * L * k / 2) + ((I_1 - I_3 - 1) * L / 2) + I_3 - 1