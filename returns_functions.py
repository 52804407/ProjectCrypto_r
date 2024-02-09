import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from dateutil import parser
import pytz
import subprocess
import click
import re
from datetime import datetime, timedelta
import os

from date_functions import (get_start_date_from_period)
from api_functions import (get_crypto_symbol)


#Function to download/load saved daily returns for each currency of the portfolio
def get_daily_returns(portfolio_percentages, start_date):
    #First we need to check if the csv file already exists and is not empty (to load data that was downloaded earlier)
    if os.path.exists("saved_daily_return_data.csv") and os.path.getsize("saved_daily_return_data.csv") > 0:
        existing_data = pd.read_csv("saved_daily_return_data.csv", index_col=0, parse_dates=True)
    else:
        #In case the csv file is empty/doesn't yet exist
        existing_data = pd.DataFrame()
    #Formate the dates to fit the yfinance functions
    start_date_formatted = get_start_date_from_period(start_date).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')
    daily_returns_dict = {}
    for currency in portfolio_percentages.keys():
        symbol = get_crypto_symbol(currency) + "-USD" #Append "-USD" as yfinance saves data based on tickers
        #Check if daily returns data for this currency and time period already exists
        if currency in existing_data.columns and not existing_data[currency].loc[start_date_formatted:end_date].isnull().all():
            daily_returns_dict[currency] = existing_data[currency].loc[start_date_formatted:end_date]
            continue
        try:
            data = yf.download(symbol, start=start_date_formatted, end=end_date)
            if not data.empty:
                daily_returns = data['Close'].pct_change()
                existing_data[currency] = daily_returns
                daily_returns_dict[currency] = daily_returns
        except Exception as e:
            print(f"Failed to download {symbol}: {str(e)}")
    #Save updated data to the saved_daily_return_data.csv file
    existing_data.to_csv("saved_daily_return_data.csv")
    return daily_returns_dict


#Function to calculate cumulative portfolio returns weighted according to the distribution of chosen portfolio type
def calculate_weighted_cumulative_returns(daily_returns_dict, portfolio_percentages):
    portfolio_returns = pd.DataFrame()
    for currency, daily_returns in daily_returns_dict.items():
        weight = portfolio_percentages[currency] / 100
        portfolio_returns[currency] = daily_returns * weight
    if not portfolio_returns.empty:
        portfolio_daily_returns = portfolio_returns.sum(axis=1)
        cumulative_returns = (1 + portfolio_daily_returns).cumprod() * 100
        return cumulative_returns
    return pd.Series()