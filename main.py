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

from slugs_mapping_tool import (crypto_mapping_top50)                           

from portfolio_functions import (calculate_equal_weights,
                                 calculate_global_minimum_variance,
                                 calculate_value_weights)

from yfinance_functions import (calculate_daily_returns,
                                #get_daily_close_price_data,
                                portfolio_manager_GMV)

#Validation function for start_date
def validate_start_date(ctx, param, value):
    # Regular expression to match the format and extract parts
    match = re.match(r"(\d+)([DWMY])$", value.upper())
    if not match:
        raise click.BadParameter("Start date must be in the format of <number><D/W/M/Y> (e.g., 31D, 12W, 6M, 1Y)")
    
    number, unit = int(match.group(1)), match.group(2)
    # Validate the number based on the unit
    if unit == "D" and not (1 <= number <= 365):
        raise click.BadParameter("Days must be between 1 and 365")
    elif unit == "W" and not (1 <= number <= 52):
        raise click.BadParameter("Weeks must be between 1 and 52")
    elif unit == "M" and not (1 <= number <= 12):
        raise click.BadParameter("Months must be between 1 and 12")
    elif unit == "Y" and not (1 <= number <= 3):
        raise click.BadParameter("Years must be between 1 and 5")
    
    return value.upper()

def get_portfolio_choice():
    print("Choose a portfolio:")
    print("1. Value Weighted")
    print("2. Equal Weighted")
    print("3. Global Minimum Variance")

    while True:
        try:
            choice = int(input("Enter the number of your choice (1-3):"))
            if 1 <= choice <= 3:
                return choice
            else:
                print("Invalid choice. Please enter a number between 1 and 3.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

@click.command()
@click.argument('currencies', nargs=-1)
@click.option("--list", "list_currencies", is_flag=True, help="List all available crypto slugs")
@click.option("--start_date", default="1M", callback=validate_start_date, show_default=True, help="Start date in the format of <number><D/W/M/Y>. Default is 1M.")

def main(currencies, list_currencies, start_date):
    if list_currencies:
        #If the user wants to list all crypto slugs, call the get_crypto_slugs function
        crypto_slugs = get_crypto_slugs()
        print("Available crypto slugs:")
        for slug in crypto_slugs:
            print(slug)
        return

    #Input for currencies
    while True: #Continue until valid input is received
        if not currencies:
            print("\nEnter up to 5 crypto slugs (e.g.: \"bitcoin ethereum solana\"), choose \"top3\" / \"top5\" by market cap or type \"list\" to list all available slugs") 
            print("(Press Enter to skip and use default portfolio (top5))")
            user_input = input().strip()
            #Replace non-alphanumeric characters (except "-") with space
            user_input = ''.join(char if char.isalnum() or char.isspace() or char == '-' else ' ' for char in user_input)
            #Split the input into a list of cryptocurrencies
            currencies = user_input.split()

            #Add the list option to display all available slugs
            if currencies == ["list"]:
                available_slugs = list(crypto_mapping_top50.keys())
                print("\nList of available crypto slugs:")
                print(available_slugs)
                currencies = [] #Reset currencies
                continue #Go back to the beginning of the loop    

            #Restrict the maximum number of currencies to 5
            if len(currencies) > 5:
                print("\nA maximum of 5 cryptocurrencies is allowed.")
                currencies = [] #Reset currencies
                continue #Go back to the beginning of the loop

            #Default currencies if user skips
            if not currencies:
                currencies = ["bitcoin", "ethereum", "tether", "bnb", "solana"]
                break
            #Add top3 choice
            if currencies == ["top3"]:
                currencies = ["bitcoin", "ethereum", "tether"]
                break
            #Add top5 choice
            if currencies == ["top5"]:
                currencies = ["bitcoin", "ethereum", "tether", "bnb", "solana"]
                break
            
            if currencies:
                break    

    #Input for time period
    print("\nEnter time period (end date is today) in the format: <number><D/W/M/Y> (e.g.: \"5D\", \"1W\", \"6M\", \"1Y\")")
    print("(Press Enter to skip and use default period (1M))")
    start_date_input = input().strip().upper()
    #Default value if user skips
    if not start_date_input:
        start_date = "1M"  
    else:
        try:
            # Validate the start_date format. Reuse the existing validate_start_date function.
            start_date = validate_start_date(None, None, start_date_input)
        except click.BadParameter as e:
            print(f"Invalid start date format. {e.message}")
            return  ### TO-DO: ASK FOR INPUT AGAIN
        
    #Function to extract start date from period
    def get_start_date_from_period(period):
        unit = period[-1]
        quantity = int(period[:-1])
        if unit == "D":
            return datetime.now() - timedelta(days=quantity)
        elif unit == "W":
            return datetime.now() - timedelta(weeks=quantity)
        elif unit == "M":
            return datetime.now() - timedelta(days=30*quantity)
        elif unit == "Y":
            return datetime.now() - timedelta(days=365*quantity)

    
    #Setting start and end dates to pass on for GMV according to user's choice (end date always today)
    start_date_dt = get_start_date_from_period(start_date)
    end_date_dt = datetime.now()
    start_date_str = start_date_dt.strftime("%Y-%m-%d")
    end_date_str = end_date_dt.strftime("%Y-%m-%d")
    
    #Choose the portfolio
    portfolio_choice = get_portfolio_choice()
    if portfolio_choice == 1:
        portfolio_percentages = calculate_value_weights(*currencies)
        portfolio_name = "Value-weighted Portfolio"
    elif portfolio_choice == 2:
        portfolio_percentages = calculate_equal_weights(*currencies)    
        portfolio_name = "Equal-weighted Portfolio"
    elif portfolio_choice == 3:
        portfolio_percentages = calculate_global_minimum_variance(*currencies, start_date=start_date_str, end_date=end_date_str)
        portfolio_name = "Global Minimum Variance Portfolio"

    #Print the resulting portfolio
    print("\nYour portfolio percentages:")
    labels = []
    sizes = []
    for currency, percentage in portfolio_percentages.items():
        print(f"{currency}: {percentage:.2f}%")
        labels.append(currency)
        sizes.append(percentage)
    print("\n(Please close the generated pie chart to continue)")

    #Pie chart of resulting portfolio distribution
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')

    plt.title(f"{portfolio_name} Distribution")
    plt.show()

    def calculate_portfolio_returns(portfolio_percentages, start_date):
        start_date_formatted = get_start_date_from_period(start_date).strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')
        
        portfolio_returns = pd.DataFrame()

        for currency, percentage in portfolio_percentages.items():
            symbol = get_crypto_symbol(currency) + "-USD"
            try:
                data = yf.download(symbol, start=start_date_formatted, end=end_date)
                if not data.empty:
                    daily_returns = data['Close'].pct_change()
                    weight = percentage / 100
                    portfolio_returns[currency] = daily_returns * weight
            except Exception as e:
                print(f"Failed to download {symbol}: {str(e)}")

        if not portfolio_returns.empty:
            #Sum the weighted returns across all currencies to get the portfolio's daily returns
            portfolio_daily_returns = portfolio_returns.sum(axis=1)
            #Calculate cumulative returns
            cumulative_returns = (1 + portfolio_daily_returns).cumprod() * 100
            
            return cumulative_returns

        return pd.Series()#If no data are available return an empty series
    
    cumulative_returns = calculate_portfolio_returns(portfolio_percentages, start_date)
    if not cumulative_returns.empty:
        cumulative_returns.plot(title="Portfolio Cumulative Returns Over Time")
        plt.xlabel("Date")
        plt.ylabel("Cumulative Returns")
        #Grid of horizontal lines only
        plt.gca().yaxis.grid(True)
        plt.gca().xaxis.grid(False)
        plt.show()
    else:
        print("No data available to plot.")

    #Ask user if they want to compare another portfolio
    compare_another = input("\nWould you like to compare returns with another portfolio? (yes/no): ").strip().lower()
    cumulative_returns_2 = None #Begin with empty cumulative_returns_2
    if compare_another == "yes":
        # Repeat the portfolio selection process
        portfolio_choice_2 = get_portfolio_choice()
        if portfolio_choice_2 == 1:
            portfolio_percentages_2 = calculate_value_weights(*currencies)
            portfolio_name_2 = "Value-weighted Portfolio"
        elif portfolio_choice_2 == 2:
            portfolio_percentages_2 = calculate_equal_weights(*currencies)    
            portfolio_name_2 = "Equal-weighted Portfolio"
        elif portfolio_choice_2 == 3:
            portfolio_percentages_2 = calculate_global_minimum_variance(*currencies, start_date=start_date_str, end_date=end_date_str)
            portfolio_name_2 = "Global Minimum Variance Portfolio"

        #Calculate cumulative returns for the second portfolio
        cumulative_returns_2 = calculate_portfolio_returns(portfolio_percentages_2, start_date)

    if not cumulative_returns.empty and cumulative_returns_2 is not None and not cumulative_returns_2.empty: #This covers the input "no"
        plt.figure(figsize=(10, 6))
        
        # Plot the first portfolio
        cumulative_returns.plot(label=f'{portfolio_name}')
        
        # Plot the second portfolio on the same figure
        cumulative_returns_2.plot(label=f'{portfolio_name_2}')
        
        plt.title("Comparison of Portfolio Performances Over Time")
        plt.xlabel("Date")
        plt.ylabel("Cumulative Returns")
        plt.legend()
        #Grid of horizontal lines only
        plt.gca().yaxis.grid(True)
        plt.gca().xaxis.grid(False)
        plt.show()

if __name__ == "__main__":
    main()