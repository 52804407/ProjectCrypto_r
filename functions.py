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






def get_market_cap(slug ="bitcoin", id = 1): #Function that obtains cryptocurency market_cap in USD.
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
    data = info['data'][f'{id}']
    symbol = data['symbol']
    market_cap = data['quote']['USD']['market_cap']
    market_cap_dict = {symbol : market_cap}
    return print(market_cap_dict)





def get_crypto_ids(slug = 'bitcoin'): #Function that obtains ID for any slug
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

    # Return the dictionary with slugs as keys and IDs as values
    return print(crypto_slugs_ids[f'{slug}'])



