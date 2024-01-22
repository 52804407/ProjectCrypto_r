#Main file to run
#Importing libraries
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from dateutil import parser
import pytz
import argparse
import subprocess

#Importing local functions from functions.py
from api_functions import (portfolio_manager, 
                        get_crypto_ids,
                        get_crypto_symbol,
                        get_market_cap,
                        get_crypto_slugs)

#from yfinance_functions import (get_daily_close_price_data,
#                                calculate_daily_returns)


# connecting to config.ini
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
default_config = config['DEFAULT']


def get_portfolio_choice():
    print("Choose a portfolio:")
    print("1. Value Weighted")
    print("2. Equal Weighted")
    print("3. Global Minimum Variance")

    while True:
        try:
            choice = int(input("Enter the number of your choice (1-3): "))
            if 1 <= choice <= 3:
                return choice
            else:
                print("Invalid choice. Please enter a number between 1 and 3.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    portfolio_choice = get_portfolio_choice()

    if portfolio_choice == 1:
        portfolio_name = "value_weighted"
    elif portfolio_choice == 2:
        portfolio_name = "equal_weighted"
    else:
        portfolio_name = "global_minimum_variance"

    subprocess.run(["python", f"{portfolio_name}.py", "-l"])

    
