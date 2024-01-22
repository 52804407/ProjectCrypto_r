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

#Importing local functions from yfinance_functions.py
from yfinance_functions import (get_daily_close_price_data, 
                        calculate_daily_returns,
                        portfolio_manager)


# connecting to config.ini
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
default_config = config['DEFAULT']

print("Enter up to 5 crypto tickers (Example: bitcoin ethereum solana) (press Enter to skip and use default portfolio):")
user_input = input().strip()
# Replace non-alphanumeric characters with space
user_input = ''.join(char if char.isalnum() or char.isspace() else ' ' for char in user_input)
# Split the input into a list of cryptocurrencies
user_input = user_input.split()

# Create ArgumentParser object
parser = argparse.ArgumentParser(description='Create a GMV portfolio.')
parser.add_argument('currencies', metavar='currency', type=str, nargs='*', help='Cryptocurrencies for the portfolio')
parser.add_argument('-l', '--list', action='store_true', help='List all available crypto slugs')
args = parser.parse_args()

#if args.list:
#    # If the user wants to list all crypto slugs, call the get_crypto_slugs function
#    crypto_slugs = get_crypto_slugs()
#    print("Available crypto slugs:")
#    for slug in crypto_slugs:
#        print(slug)

# If no input provided, use user input or defaults
if not args.currencies:
    currencies = user_input
    if not currencies:
        currencies = ['BTC-USD', 'ETH-USD', 'SOL-USD']
else:
    currencies = args.currencies

crypto_mapping_top50 = {
    "bitcoin": "BTC-USD",
    "ethereum": "ETH-USD",
    "tether": "USDT-USD",
    "binancecoin": "BNB-USD",
    "solana": "SOL-USD",
    "xrp": "XRP-USD",
    "usdcoin": "USDC-USD",
    "lidostakedeth": "STETH-USD",
    "cardano": "ADA-USD",
    "dogecoin": "DOGE-USD",
    "avalanche": "AVAX-USD",
    "bitbegin": "BRIT-USD",
    "tron": "TRX-USD",
    "wrappedtron": "WTRX-USD",
    "chainlink": "LINK-USD",
    "polkadot": "DOT-USD",
    "toncoin": "TON11419-USD",
    "polygon": "MATIC-USD",
    "wrappedbitcoin": "WBTC-USD",
    "shibainu": "SHIB-USD",
    "dai": "DAI-USD",
    "litecoin": "LTC-USD",
    "internetcomputer": "ICT-USD",
    "bitcoincash": "BCH-USD",
    "leo": "LEO-USD",
    "uniswap": "UNI7083-USD",
    "cosmos": "ATOM-USD",
    "ethereumclassic": "ETC-USD",
    "stellar": "XLM-USD",
    "okb": "OKB-USD",
    "injective": "INJ-USD",
    "optimism": "OP-USD",
    "monero": "XMR-USD",
    "near": "NEAR-USD",
    "aptos": "APT21794-USD",
    "firstdigitalusd": "FDUSD-USD",
    "filecoin": "FIL-USD",
    "wrappedeos": "WEOS-USD",
    "celestia": "TIA22861-USD",
    "lidodao": "LDO-USD",
    "hedera": "HBAR-USD",
    "wrappedhbar": "WHBAR-USD",
    "immutable": "IMX10603-USD",
    "kaspa": "KAS-USD",
    "arbitrum": "ARB11841-USD",
    "bitcoinbep2": "BTCB-USD",
    "mantle": "MNT27075-USD",
    "stacks": "STX4847-USD",
    "cronos": "CRO-USD",
    "vechain": "VET-USD"
}

#Function to convert user input (e.g. bitcoin) to ticker symbols (e.g. BTC-USD)
def convert_to_tickers(user_input, mapping):
    return [mapping[currency.lower()] for currency in user_input if currency.lower() in mapping]

currencies = convert_to_tickers(currencies, crypto_mapping_top50)


# Call the portfolio_manager function with user-selected cryptocurrencies
portfolio_percentages = portfolio_manager(*currencies)
print(portfolio_percentages)
# Print the resulting portfolio
#print("\nYour portfolio percentages:")
#labels = []
#sizes = []
#for currency, percentage in portfolio_percentages.items():
#    print(f"{currency}: {percentage:.2f}%")
#    labels.append(currency)
#    sizes.append(percentage)
    
# Pie chart of resulting portfolio
#fig1, ax1 = plt.subplots()
#ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
#ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

#plt.title("Crypto Portfolio Distribution")
#plt.show()