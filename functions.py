import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import configparser
from dateutil import parser
import pytz






def get_market_cap(slug ="bitcoin", id = 1): #Function that obtains cryptocurency market_cap in USD from coinmarketcap API
    # Read the API key from the config.ini file
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_key = config['DEFAULT']['API_KEY']

    # Set up the request parameters and headers
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = { 'slug': f'{slug}', 'convert': 'USD' }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key
    }
    # Send the request and retrieve the response
    session = Session()
    session.headers.update(headers)
    response = session.get(url, params=parameters)
    info = json.loads(response.text)

    # Extract the desired information from the response
    data = info['data'].get(str(id))  # Use .get() to handle the case where id is not found
    if data:
        symbol = data['symbol']
        market_cap = data['quote']['USD']['market_cap']
        market_cap_dict = {symbol: market_cap}
        return market_cap_dict
    else:
        print(f"Currency with ID '{id}' not found")
        return {}  # Return an empty dictionary if currency is not found



def get_crypto_ids(slug = 'bitcoin'): #Function that obtains ID for any slug from coinmarketcap API
    # Read the API key from the config.ini file
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_key = config['DEFAULT']['API_KEY']

    # Set up the request parameters and headers
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key
    }
    # Send the request and retrieve the response
    session = Session()
    session.headers.update(headers)
    response = session.get(url)
    info = json.loads(response.text)

    # Extract the desired information from the response
    crypto_data = info['data']

    # Process the crypto data
    crypto_slugs_ids = {}
    for crypto in crypto_data:
        crypto_id = crypto['id']
        crypto_name = crypto['name']
        crypto_slug = crypto['slug']
        crypto_slugs_ids[crypto_slug] = crypto_id

        # Check if the slug exists in the data
    if slug not in crypto_slugs_ids:
        raise ValueError(f"Currency with slug '{slug}' not found")

    # Return the slug ID
    return crypto_slugs_ids[slug]




def portfolio_manager(*currencies):
    # Ensure there are at most 5 currencies
    if len(currencies) > 5:
        raise ValueError("Up to 5 currencies are allowed")

    # Get market cap for each currency
    market_caps = {}
    for currency in currencies:
        try:
            crypto_id = get_crypto_ids(slug=currency)
            market_cap_dict = get_market_cap(slug=currency, id=crypto_id)

            # Skip if market cap is None
            if market_cap_dict is not None and currency in market_cap_dict:
                market_caps[currency] = market_cap_dict[currency]
        except ValueError as e:
            print(e)

    # If no valid currencies found, print a message
    if not market_caps:
        print("No valid currencies found")
    else:
        # Calculate total market cap
        total_market_cap = sum(market_caps.values())

        # Calculate and print percentages for each currency
        percentages = {currency: market_cap / total_market_cap * 100 for currency, market_cap in market_caps.items()}
        print(percentages)

        return percentages

# Test usage (isn't working yet, get_market_cap() and get_crypto_ids() works correctly, problem is is portfolio_manager() )
result = portfolio_manager('bitcoin', 'ethereum')
print(result)