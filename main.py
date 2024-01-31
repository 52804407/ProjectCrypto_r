# Importing libraries
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
import configparser
import click

from api_functions import (get_crypto_slugs,
                           portfolio_manager,
                           get_crypto_ids,
                           get_crypto_symbol,
                           get_market_cap)

                           

from portfolio_functions import (calculate_equal_weights,
                                 calculate_global_minimum_variance,
                                 calculate_value_weights)

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

@click.command()
@click.argument('currencies', nargs=-1)
@click.option('--list', 'list_currencies', is_flag=True, help='List all available crypto slugs')

def main(currencies, list_currencies):
    if list_currencies:
        # If the user wants to list all crypto slugs, call the get_crypto_slugs function
        crypto_slugs = get_crypto_slugs()
        print("Available crypto slugs:")
        for slug in crypto_slugs:
            print(slug)
        return

    # If no input provided, use user input or defaults
    if not currencies:
        print("Enter up to 5 crypto slugs (Example: bitcoin ethereum solana) (press Enter to skip and use default portfolio):")
        user_input = input().strip()
        # Replace non-alphanumeric characters with space
        user_input = ''.join(char if char.isalnum() or char.isspace() else ' ' for char in user_input)
        # Split the input into a list of cryptocurrencies
        currencies = user_input.split()
        if not currencies:
            currencies = ['bitcoin', 'ethereum', 'solana']

    portfolio_choice = get_portfolio_choice()

    if portfolio_choice == 1:
        portfolio_percentages = calculate_value_weights(*currencies)
    elif portfolio_choice == 2:
        portfolio_percentages = calculate_equal_weights(*currencies)    
    elif portfolio_choice == 3:
        portfolio_percentages = calculate_global_minimum_variance(*currencies)
        

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

    plt.title("Value-Weighted Portfolio Distribution")
    plt.show()

    

if __name__ == "__main__":
    main()