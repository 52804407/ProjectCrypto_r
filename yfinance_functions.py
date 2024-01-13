import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt




#Function to download daily close price data
def get_daily_close_price_data(*currencies):
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
#print(close_data)

#Function calculating daily returns
def calculate_daily_returns(*currencies):
    daily_returns = get_daily_close_price_data(currencies)/get_daily_close_price_data(currencies).shift(1)
    return daily_returns

daily_returns = calculate_daily_returns(currencies)
print(daily_returns)