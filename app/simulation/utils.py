import math


def simulate_position(usd_to_invest: float, duration_years: float, price_one_usd: float, price_two_usd: float,
                      trading_fees: float, borrow_rate_one: float, borrow_rate_two: float):
    """
    Returns the values necessary to plot a graph of the value of the long position, short position and total position against the price of the asset.

    :param float usd_to_invest: The amount to invest, in USD.
    :param float duration_years: The amount of time to invest for, in years.
    :param float price_one_usd: The price of the first token, in USD.
    :param float price_two_usd: The price of the second token, in USD.
    :param float trading_fees: The average interest earned on invested tokens, as a percentage.
    :param float borrow_rate_one: The interest rate for borrowing the first token, as a percentage.
    :param float borrow_rate_one: The interest rate for borrowing the second token, as a percentage.
    """
    
    price_range = [x * price_two_usd / 50 for x in range(200)]

    long_quantity = usd_to_invest * (1/4) / price_one_usd
    long_values = __simulate_long_position(long_quantity, duration_years, price_one_usd, price_two_usd, trading_fees, borrow_rate_one, price_range)

    short_quantity = usd_to_invest * (3/4) / price_one_usd
    short_values = __simulate_short_position(short_quantity, duration_years, price_two_usd, trading_fees, borrow_rate_two, price_range)

    total_values = [sum(x) for x in zip(long_values, short_values)]

    return price_range, long_values, short_values, total_values


def __simulate_long_position(value_invested: float, duration_years: float, price_token_one: float, price_token_two: float,
                             trading_fees: float, borrow_rate_one: float, price_range: list[float]):

    token_one_borrowed = value_invested / price_token_one * 2
    total_value_invested = value_invested * 3

    token_one_owed = token_one_borrowed * math.exp(borrow_rate_one * duration_years)

    results = []
    for future_price in price_range:
        
        asset_value = total_value_invested * math.sqrt(future_price / price_token_two) * math.exp(trading_fees * duration_years)
        net_asset_value = asset_value - token_one_owed * price_token_one
        results.append(net_asset_value - value_invested)

    return results


def __simulate_short_position(value_invested: float, duration_years: float, price_token_two: float,
                              trading_fees: float, borrow_rate_two: float, price_range: list[float]):
    
    token_two_borrowed = value_invested / price_token_two * 2
    total_value_invested = value_invested * 3

    token_two_owed = token_two_borrowed * math.exp(borrow_rate_two * duration_years)

    results = []
    for future_price in price_range:
        
        asset_value = total_value_invested * math.sqrt(future_price / price_token_two) * math.exp(trading_fees * duration_years)
        net_asset_value = asset_value - token_two_owed * future_price
        results.append(net_asset_value - value_invested)

    return results
