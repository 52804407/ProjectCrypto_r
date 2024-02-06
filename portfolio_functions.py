import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

from api_functions import (get_crypto_slugs,
                           portfolio_manager,
                           get_crypto_ids,
                           get_crypto_symbol,
                           get_market_cap)

from slugs_mapping_tool import (crypto_mapping_top50,
                                convert_to_tickers,
                                convert_to_names)

from yfinance_functions import (calculate_daily_returns,
                                #get_daily_close_price_data,
                                portfolio_manager_GMV)

# Equal_weighted portfolio
def calculate_equal_weights(*currencies):
    percentages = {}
    equal_weight = 1/len(currencies)
    for currency in currencies:
        percentages[currency] = equal_weight*100
    return percentages

# Value_weighted portfolio (based on live market capitalization)
def calculate_value_weights(*currencies): 
    # Ensure there are at most 5 currencies
    if len(currencies) > 5:
        raise ValueError("Up to 5 currencies are allowed")
    # Get market cap for each currency
    market_caps = {}
    for currency in currencies:
        try:
            crypto_id = get_crypto_ids(slug=currency)
            market_cap_dict = get_market_cap(slug=currency, id=crypto_id)
            crypto_symbol = get_crypto_symbol(slug = currency)
            # Skip if market cap is None
            if market_cap_dict is not None and crypto_symbol in market_cap_dict:
                market_caps[currency] = market_cap_dict[crypto_symbol]        
        except ValueError as e:
            print(e)
    # If no valid currencies found, print a message
    if not market_caps:
        print("No valid currencies found")
    else:
        # Calculate total market cap
        total_market_cap = sum(market_caps.values())
        # Calculate and print percentages for each currency
        percentages = {currency: market_cap / total_market_cap * 100 for currency, market_cap in market_caps.items()}
        return percentages


# Global_minimum_variance portfolio
#convert user input to ticker symbol
def calculate_global_minimum_variance(*currencies):

    currencies = convert_to_tickers(currencies, crypto_mapping_top50)

    #Call the portfolio_manager function with user-selected cryptocurrencies
    #portfolio_percentages = portfolio_manager2(*currencies)
    #daily_returns = calculate_daily_returns(*currencies)
    GMV_percentages = portfolio_manager_GMV(*currencies)
    #Convert tickers back to names
    GMV_percentages = {convert_to_names(crypto_mapping_top50).get(ticker, ticker): percentage for ticker, percentage in GMV_percentages.items()}
    return GMV_percentages
currencies = ["bitcoin", "ethereum"]
print(calculate_global_minimum_variance(*currencies))