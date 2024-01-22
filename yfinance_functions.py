import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

    return daily_returns


currencies = ["BTC-USD","ETH-USD"]
print(calculate_daily_returns(*currencies)["BTC-USD"])