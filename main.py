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
import re
from datetime import datetime, timedelta

from api_functions import (get_crypto_slugs,
                           portfolio_manager,
                           get_crypto_ids,
                           get_crypto_symbol,
                           get_market_cap)

                           

from portfolio_functions import (calculate_equal_weights,
                                 calculate_global_minimum_variance,
                                 calculate_value_weights)

from yfinance_functions import (calculate_daily_returns,
                                #get_daily_close_price_data,
                                portfolio_manager_GMV)

# Enhanced validation function for start_date
def validate_start_date(ctx, param, value):
    # Regular expression to match the format and extract parts
    match = re.match(r'(\d+)([DWMY])$', value.upper())
    if not match:
        raise click.BadParameter('Start date must be in the format of <number><D/W/M/Y> (e.g., 31D, 12W, 6M, 1Y)')
    
    number, unit = int(match.group(1)), match.group(2)
    # Validate the number based on the unit
    if unit == 'D' and not (1 <= number <= 365):
        raise click.BadParameter('Days must be between 1 and 365')
    elif unit == 'W' and not (1 <= number <= 52):
        raise click.BadParameter('Weeks must be between 1 and 52')
    elif unit == 'M' and not (1 <= number <= 12):
        raise click.BadParameter('Months must be between 1 and 12')
    elif unit == 'Y' and number != 1:
        raise click.BadParameter('Years must be 1')
    
    return value.upper()

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
@click.option('--start_date', default='1D', callback=validate_start_date, show_default=True, help="Start date in the format of <number><D/W/M/Y>. Default is 1D.")

def main(currencies, list_currencies, start_date):
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

    print("Enter a start date in the format of <number><D/W/M/Y> (e.g., 31D, 12W, 6M, 1Y) or press Enter to use default (1D):")
    start_date_input = input().strip().upper()
    if not start_date_input:
        start_date = '1D'  # Default value if user skips
    else:
        try:
            # Validate the start_date format. Reuse the existing validate_start_date function.
            start_date = validate_start_date(None, None, start_date_input)
        except click.BadParameter as e:
            print(f"Invalid start date format. {e.message}")
            return  # Exit the function or ask for the input again based on your preference


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

    def get_start_date_from_period(period):
        unit = period[-1]
        quantity = int(period[:-1])
        if unit == 'D':
            return datetime.now() - timedelta(days=quantity)
        elif unit == 'W':
            return datetime.now() - timedelta(weeks=quantity)
        elif unit == 'M':
            return datetime.now() - timedelta(days=30*quantity)  # Approximation
        elif unit == 'Y':
            return datetime.now() - timedelta(days=365*quantity)  # Approximation

# Function to fetch historical data and calculate returns
    def calculate_portfolio_returns(portfolio_percentages, start_date, initial_investment=1000):
        start_date_actual = get_start_date_from_period(start_date).strftime('%Y-%m-%d')
        end_date_actual = datetime.now().strftime('%Y-%m-%d')
        
        portfolio_returns = pd.DataFrame()
        
        for currency, percentage in portfolio_percentages.items():
            # Append '-USD' to each currency symbol
            symbol = get_crypto_symbol(currency) + '-USD'
            try:
                data = yf.download(symbol, start=start_date_actual, end=end_date_actual)
                
                # Calculate daily returns
                daily_returns = data['Adj Close'].pct_change()
                
                # Calculate weighted returns
                weight = percentage / 100
                portfolio_returns[currency] = daily_returns * weight
            except Exception as e:
                print(f"Failed to download {symbol}: {str(e)}")
        
        if not portfolio_returns.empty:
            # Calculate portfolio daily returns
            portfolio_daily_returns = portfolio_returns.sum(axis=1)
            
            # Calculate cumulative returns and normalize starting value to 100%
            cumulative_returns = (1 + portfolio_daily_returns).cumprod() * 100
            
            # Plotting
            plt.figure(figsize=(10, 6))
            plt.plot(cumulative_returns.index, cumulative_returns, label='Portfolio Performance')
            plt.title('Portfolio Performance Over Time')
            plt.xlabel('Date')
            plt.ylabel('Performance (%)')
            plt.legend()
            plt.grid(True)
            plt.show()
            
            # Calculate and print the portfolio difference in %
            starting_value = 100  # Starting at 100%
            ending_value = cumulative_returns.iloc[-1]  # Last value in the series
            performance_difference = ending_value - starting_value
            print(f"Portfolio performance from start to end date: {performance_difference:.2f}% difference.")
        else:
            print("No data available to plot.")


    calculate_portfolio_returns(portfolio_percentages, start_date, 1000)

if __name__ == "__main__":
    main()