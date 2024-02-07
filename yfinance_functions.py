import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

#Function to download daily close price data
#def get_daily_close_price_data(*currencies):
#    if len(currencies) > 5:
#        raise ValueError("Up to 5 currencies are allowed")
#    elif len(currencies) > 1:
#        # Initialize a dictionary to hold close data for each currency
#        close_data = {}
#        for currency in currencies:
#            ticker = yf.Ticker(currency)
#            data = ticker.history()
#            close_data[currency] = data["Close"]
#    elif len(currencies) == 1:
#        ticker = yf.Ticker(currencies[0])
#        data = ticker.history()
#        close_data = {currencies[0]: data["Close"]}
#    return close_data

#Function calculating daily returns
def calculate_daily_returns(*currencies, start_date, end_date):
    close_data = pd.DataFrame()
    daily_returns = pd.DataFrame()
    for currency in currencies:
        ticker = yf.Ticker(currency)
        close_data[currency] = ticker.history(start=start_date, end=end_date)["Close"]
        daily_returns[currency] = close_data[currency] / close_data[currency].shift(1) - 1
    return daily_returns

# Function that calculates how should be porfolio managed in % based on GMV
def portfolio_manager_GMV(*currencies, start_date, end_date): 
    # Ensure there are at most 5 currencies
    if len(currencies) > 5:
        raise ValueError("Up to 5 currencies are allowed")
    #Insert return from calculate_daily_returns function
    daily_returns = calculate_daily_returns(*currencies, start_date=start_date, end_date=end_date)
    #Calculate the cov matrix
    daily_returns_cov_matrix = daily_returns.cov()

    ##Constraint functions for optimization
    def portfolio_variance(weights):
        return weights.T @ daily_returns_cov_matrix @ weights

    def check_sum(weights):
        return np.sum(weights) - 1

    #We need to specify an initial guess 
    #Equal weighted portfolio
    init_guess = []
    for i in range(len(currencies)):
        init_guess.append(1 / len(currencies))
    #Back-loaded portfolio
    #init_guess = [0.5 / (len(currencies) - 1) for i in range(len(currencies) - 1)] + [0.5]
    #Front-loaded portfolio
    #init_guess = [0.5] + [0.5 / (len(currencies) - 1) for _ in range(len(currencies) - 1)]
    
    #Limit each percentage to be between 0 and 1
    bounds = tuple((0, 1) for i in range(len(currencies)))
    #Set constraints so that percentages sum to 1 
    constraints = ({'type': 'eq', 'fun': check_sum})

    #Specify options to increase GMV iterations and adjust tolerance (to make GMV optimizations more precise)
    options = {
        'maxiter': 100000,
        'ftol': 1e-6,
        'disp': False
    }

    #Minimize the portfolio variance using SLSQP
    opt_results = minimize(portfolio_variance, init_guess, method="SLSQP", bounds=bounds, constraints=constraints, options=options)
    #Save percentages in a dictionary for each currency
    percentages = dict(zip(currencies, opt_results.x*100))

    return percentages
