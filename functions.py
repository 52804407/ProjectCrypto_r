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

def get_info():
    # Read the API key from the coinmarket.ini file
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_key = config['DEFAULT']['API_KEY']

    # Set up the request parameters and headers
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = { 'slug': 'bitcoin', 'convert': 'USD' }
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
    data = info['data']['1']
    name = data['name']
    symbol = data['symbol']
    rank = data['cmc_rank']
    total_supply = data['total_supply']
    circulating_supply = data['circulating_supply']
    market_cap = data['quote']['USD']['market_cap']
    price = data['quote']['USD']['price']
    market_cap_dominance = data['quote']['USD']['market_cap_dominance']
    percent_change_1h = data['quote']['USD']['percent_change_1h']
    percent_change_24h = data['quote']['USD']['percent_change_24h']
    volume_24h = data['quote']['USD']['volume_24h']
    volume_change_24h = data['quote']['USD']['volume_change_24h']
    timestamp = info['status']['timestamp']

    # Convert the timestamp to a timezone-aware datetime object
    timestamp_local = parser.parse(timestamp).astimezone(pytz.timezone('Turkey'))
    

    # Format the timestamp as desired
    formatted_timestamp = timestamp_local.strftime('%Y-%m-%d %H:%M:%S')

    # Print the information
    print(f'Name: {name}, Symbol: {symbol}, Price: {price:,.2f}, Percent change (1h): {percent_change_1h}, Percent change (24h): {percent_change_24h}, Total supply: {total_supply}, Circulating supply: {circulating_supply}, Market capitalization: {market_cap}, Market capitalization dominance: {market_cap_dominance}, Volume (24h): {volume_24h}, Volume change (24h): {volume_change_24h}, Timestamp: {formatted_timestamp}')

get_info()