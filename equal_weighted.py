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

#Connecting to config.ini
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
default_config = config['DEFAULT']

print("Enter up to 5 crypto slugs (Example: bitcoin ethereum solana) (press Enter to skip and use default portfolio):")
user_input = input().strip()
#Replace non-alphanumeric characters with space
user_input = ''.join(char if char.isalnum() or char.isspace() else ' ' for char in user_input)
#Split the input into a list of cryptocurrencies
user_input = user_input.split()

#Create ArgumentParser object
parser = argparse.ArgumentParser(description='Create a portfolio based on cryptocurrency market caps.')
parser.add_argument('currencies', metavar='currency', type=str, nargs='*', help='Cryptocurrencies for the portfolio')
parser.add_argument('-l', '--list', action='store_true', help='List all available crypto slugs')
args = parser.parse_args()


from api_functions import (get_crypto_slugs)

if args.list:
    #If the user wants to list all crypto slugs, call the get_crypto_slugs function
    crypto_slugs = get_crypto_slugs()
    print("Available crypto slugs:")
    for slug in crypto_slugs:
        print(slug)

#If no input provided, use user input or defaults
if not args.currencies:
    currencies = user_input
    if not currencies:
        currencies = ['bitcoin', 'ethereum', 'solana']
else:
    currencies = args.currencies

#Function calculating equal weights
def calculate_equal_weights(*currencies):
    percentages = {}
    equal_weight = 1/len(currencies)
    for currency in currencies:
        percentages[currency] = equal_weight*100
    return percentages

portfolio_percentages = calculate_equal_weights(*currencies)

#Print the resulting portfolio
print("\nYour portfolio percentages:")
labels = []
sizes = []
for currency, percentage in portfolio_percentages.items():
    print(f"{currency}: {percentage:.2f}%")
    labels.append(currency)
    sizes.append(percentage)
    
#Pie chart of resulting portfolio
fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')

plt.title("Equal-Weighted Portfolio Distribution")
plt.show()