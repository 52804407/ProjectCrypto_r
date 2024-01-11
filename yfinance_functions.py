import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt




#Function to download daily close price data for the specified tickers and time period:
def get_daily_close_price_data(currencies):
    if len(currencies)>1:
        tickers = yf.Tickers(currencies)
        data = tickers.history()
    else:
        tickers = yf.Ticker(currencies[0])
        data = tickers.history()
    if len(currencies) > 1:
        close_data = data["Close"]
    else:
        close_data = data[["Close"]]
    return close_data

currencies = ["BTC-USD","ETH-USD"]
close_data = get_daily_close_price_data(currencies)
print(close_data)
