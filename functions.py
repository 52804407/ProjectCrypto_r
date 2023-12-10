import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

#Function to obtain live marketcap from CoinMarketCap API, standard api_key is our, we suggest to create your own on coinmarketcap.com
def market_cap(api_key = 5ceece0b-74a3-49ee-85a2-513efdf7539f):
  url = 'https://pro-api.coinmarketcap.com'
  parameters = {
    'start':'1',
    'limit':'5000',
    'convert':'USD'
  }
  headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': f'{api_key}',
  }

  session = Session()
  session.headers.update(headers)

  try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    print(data)
  except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)
