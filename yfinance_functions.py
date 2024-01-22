import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

#Function to download daily close price data
def get_daily_close_price_data(*currencies):
    if len(currencies) > 5:
        raise ValueError("Up to 5 currencies are allowed")
    elif len(currencies) > 1:
        # Initialize a dictionary to hold close data for each currency
        close_data = {}
        for currency in currencies:
            ticker = yf.Ticker(currency)
            data = ticker.history()
            close_data[currency] = data["Close"]
    elif len(currencies) == 1:
        ticker = yf.Ticker(currencies[0])
        data = ticker.history()
        close_data = {currencies[0]: data["Close"]}
    return close_data

#Function calculating daily returns
def calculate_daily_returns(*currencies):
    # Get the close price data
    close_data = get_daily_close_price_data(*currencies)
    
    # Initialize a dictionary to hold daily returns for each currency
    daily_returns = {}

    # Calculate daily returns for each currency
    for currency in currencies:
        # Avoid division by zero and cases where there's no previous day data
        if close_data[currency].empty or close_data[currency].shape[0] < 2:
            continue
        
        # Calculate the daily returns
        daily_returns[currency] = close_data[currency] / close_data[currency].shift(1) - 1

    return pd.DataFrame(daily_returns)


#currencies = ["BTC-USD","ETH-USD","ADA-USD","SOL-USD","BNB-USD"]
#print(calculate_daily_returns(*currencies)["BTC-USD"])


# Function that calculates how should be porfolio managed in % based on GMV
def portfolio_manager(*currencies): 
    # Ensure there are at most 5 currencies
    if len(currencies) > 5:
        raise ValueError("Up to 5 currencies are allowed")
    #Insert return from calculate_daily_returns function
    daily_returns = calculate_daily_returns(*currencies)
    #Calculate the cov matrix
    daily_returns_cov_matrix = daily_returns.cov()

    #Constraint functions for optimization
    def portfolio_variance(weights):
        return weights.T @ daily_returns_cov_matrix @ weights

    def check_sum(weights):
        return np.sum(weights) - 1

    #We need to specify an initial guess (equal weighted portfolio)
    init_guess = []
    for i in range(len(currencies)):
        init_guess.append(1 / len(currencies))

    #Limit each percentage to be between 0 and 1
    bounds = tuple((0, 1) for i in range(len(currencies)))
    #Set constraints so that percentages sum to 1 
    constraints = ({'type': 'eq', 'fun': check_sum})

    #Minimize the portfolio variance using SLSQP
    opt_results = minimize(portfolio_variance, init_guess, method='SLSQP', bounds=bounds, constraints=constraints)
    #Save percentages in a dictionary for each currency
    percentages = dict(zip(currencies, opt_results.x*100))

    return percentages

#print(portfolio_manager(*currencies))
