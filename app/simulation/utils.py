import math


def simulate_position(usd_to_invest: float, duration_days: int, token_a_price: float, token_b_price: float, trading_fee_rate: float,
                      token_a_rate: float, token_b_rate: float) -> tuple[list[float], list[float], list[float], list[float]]:
    """
    Returns the values necessary to plot a graph of the value of the long position, short position and total position against the price of the asset.

    :param float usd_to_invest: The amount to invest, in USD.
    :param float duration_days: The amount of time to invest for, in days.
    :param float token_a_price: The price of the first token, in USD.
    :param float token_b_price: The price of the second token, in USD.
    :param float trading_fee_rate: The average interest earned on invested tokens, as a percentage.
    :param float token_a_rate: The interest rate for borrowing the first token, as a percentage.
    :param float token_b_rate: The interest rate for borrowing the second token, as a percentage.
    """
    
    labels = [f"{x - 100}%" for x in range(25, 200, 5)]
    price_range = [token_b_price * (x / 100) for x in range(25, 200, 5)]

    borrowed_a = (1/2) * usd_to_invest / token_a_price
    borrowed_b = (3/2) * usd_to_invest / token_b_price

    # Assumes no transaction fees when exchanging between USD, Token A and Token B
    long_quant_a = (3/8) * usd_to_invest / token_a_price
    long_quant_b = (3/8) * usd_to_invest / token_b_price

    short_quant_a = (9/8) * usd_to_invest / token_a_price
    short_quant_b = (9/8) * usd_to_invest / token_b_price

    long_const_prod = long_quant_a * long_quant_b
    short_const_prod = short_quant_a * short_quant_b

    long_equity = (long_quant_a - borrowed_a) * token_a_price + long_quant_b * token_b_price
    short_equity = short_quant_a * token_a_price + (short_quant_b - borrowed_b) * token_b_price

    long_profits = []
    short_profits = []
    total_profits = []

    # Assumes that the price of token a is constant (i.e. a stablecoin)
    for new_token_b_price in price_range:
        
        new_borrowed_a = borrowed_a * math.exp(token_a_rate * duration_days / 365)
        new_borrowed_b = borrowed_b * math.exp(token_b_rate * duration_days / 365)

        new_long_quant_a = math.sqrt(long_const_prod * new_token_b_price / token_a_price)
        new_long_quant_b = math.sqrt(long_const_prod / new_token_b_price * token_a_price)

        new_short_quant_a = math.sqrt(short_const_prod * new_token_b_price / token_a_price)
        new_short_quant_b = math.sqrt(short_const_prod / new_token_b_price * token_a_price)

        new_long_value = new_long_quant_a * token_a_price + new_long_quant_b * new_token_b_price
        new_short_value = new_short_quant_a * token_a_price + new_short_quant_b * new_token_b_price

        new_long_equity = new_long_value * math.exp(trading_fee_rate * duration_days / 365) - new_borrowed_a * token_a_price
        new_short_equity = new_short_value * math.exp(trading_fee_rate * duration_days / 365) - new_borrowed_b * new_token_b_price

        long_profit = new_long_equity - long_equity
        short_profit = new_short_equity - short_equity
        total_profit = long_profit + short_profit

        long_profits.append(long_profit)
        short_profits.append(short_profit)
        total_profits.append(total_profit)

    return labels, long_profits, short_profits, total_profits
