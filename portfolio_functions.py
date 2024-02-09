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

from GMV_functions import (portfolio_manager_GMV)

# Equal_weighted portfolio
def calculate_equal_weights(*currencies):
    percentages = {}
    equal_weight = 1/len(currencies)
    for currency in currencies:
        percentages[currency] = equal_weight*100
    return percentages

# Value_weighted portfolio (based on live market capitalization)
def calculate_value_weights(*currencies): 
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
    #If market cap not available for chosen currencies, print error message
    if not market_caps:
        print("No valid currencies found")
    else:
        #Calculate total market cap
        total_market_cap = sum(market_caps.values())
        #Calculate and print percentages for each currency based on market cap share of total
        percentages = {currency: market_cap / total_market_cap * 100 for currency, market_cap in market_caps.items()}
        return percentages


#Global_minimum_variance portfolio
def calculate_global_minimum_variance(*currencies, start_date, end_date):
    #Convert user input to ticker symbol
    currencies = convert_to_tickers(currencies, crypto_mapping_top50)
    #Call the portfolio_manager function with user-selected cryptocurrencies
    GMV_percentages = portfolio_manager_GMV(*currencies, start_date=start_date, end_date=end_date)
    #Convert tickers back to names
    GMV_percentages = {convert_to_names(crypto_mapping_top50).get(ticker, ticker): percentage for ticker, percentage in GMV_percentages.items()}
    return GMV_percentages
