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

#Importing local functions from functions.py
from api_functions import (portfolio_manager, 
                        get_crypto_ids,
                        get_crypto_symbol,
                        get_market_cap,
                        get_crypto_slugs)


# connecting to config.ini
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
default_config = config['DEFAULT']



# Main function
if __name__ == "__main__":
    
    print("FOR LIST OF CRYPTO SLUGS USE:  python main.py -l ")
    print("Enter up to 5 crypto slugs (Example: bitcoin ethereum solana) (press Enter to skip and use default portfolio):")
    user_input = input().strip()
    # Replace non-alphanumeric characters with space
    user_input = ''.join(char if char.isalnum() or char.isspace() else ' ' for char in user_input)
    # Split the input into a list of cryptocurrencies
    user_input = user_input.split()

    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description='Create a portfolio based on cryptocurrency market caps.')
    parser.add_argument('currencies', metavar='currency', type=str, nargs='*', help='Cryptocurrencies for the portfolio')
    parser.add_argument('-l', '--list', action='store_true', help='List all available crypto slugs')
    args = parser.parse_args()

    if args.list:
        # If the user wants to list all crypto slugs, call the get_crypto_slugs function
        crypto_slugs = get_crypto_slugs()
        print("Available crypto slugs:")
        for slug in crypto_slugs:
            print(slug)

    # If no input provided, use user input or defaults
    if not args.currencies:
        currencies = user_input
        if not currencies:
            currencies = ['bitcoin', 'ethereum', 'solana']
    else:
        currencies = args.currencies

    # Call the portfolio_manager function with user-selected cryptocurrencies
    portfolio_percentages = portfolio_manager(*currencies)

    # Print the resulting portfolio
    print("\nYour portfolio percentages:")
    for currency, percentage in portfolio_percentages.items():
        print(f"{currency}: {percentage:.2f}%")
