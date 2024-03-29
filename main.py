# Importing libraries and functions from different files
import matplotlib.pyplot as plt
import click
from datetime import datetime
import os

from slugs_mapping_tool import (crypto_mapping_top50)                           

from portfolio_functions import (calculate_equal_weights,
                                 calculate_global_minimum_variance,
                                 calculate_value_weights)

from date_functions import(validate_start_date,
                           get_start_date_from_period)

from returns_functions import (get_daily_returns,
                               calculate_weighted_cumulative_returns)

def get_portfolio_choice():
    print("Choose a portfolio:")
    print("1. Value Weighted (based on live market cap from API)")
    print("2. Equal Weighted")
    print("3. Global Minimum Variance (might yield equal weighted results in some cases)")

    while True:
        try:
            choice = int(input("Enter the number of your choice (1-3):"))
            if 1 <= choice <= 3:
                return choice
            else:
                print("\nInvalid choice. Please enter a number between 1 and 3.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

@click.command()
@click.argument('currencies', nargs=-1)
@click.option("--start_date", default="1M", callback=validate_start_date, show_default=True, help="Period in the format of <number><D/W/M/Y>. Default is 1M.")


def main(currencies, start_date):
    
    #Input for currencies to build the portfolio
    while True:  #Continue until valid input is received
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
            continue  #Go back to the beginning of the loop    

        #Restrict the maximum number of currencies to 5
        if len(currencies) > 5:
            print("\nA maximum of 5 cryptocurrencies is allowed.")
            continue  #Again, go back to the beginning of the loop

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

        #Check if all entered currencies are in the available crypto slugs
        invalid_slugs = [slug for slug in currencies if slug not in crypto_mapping_top50.keys()]
        if invalid_slugs:
            print(f"\nInvalid slug(s): {', '.join(invalid_slugs)}. Please enter valid crypto slugs.")
            continue  #Go back to the beginning of the loop

        break #All entries valid -> exit loop    


    #Input for time period
    while True:  # Loop until valid input is received
        print("\nEnter time period (end date is today) in the format: <number><D/W/M/Y> (e.g.: \"5D\", \"1W\", \"6M\", \"1Y\")")
        print("(Press Enter to skip and use default period (1M))")
        start_date_input = input().strip().upper()

        if not start_date_input:
            start_date = "1M"  #Default value if input is empty
            break
        else:
            try:
                #Validate the start_date format using the existing function
                start_date = validate_start_date(None, None, start_date_input)
                break  #If validation successful, exit
            except click.BadParameter as e:
                print(f"\nInvalid period format. {e.message}")


    #For GMV set start and end dates according to user's choice (end date always today)
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


    #Calculate cumulative portofolio returns using returns_functions.py
    daily_returns_dict = get_daily_returns(portfolio_percentages, start_date)
    cumulative_returns = calculate_weighted_cumulative_returns(daily_returns_dict, portfolio_percentages)


    #Plot cumulative portfolio returns over time
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
    while True:  #Continue until valid input is received
        compare_another = input("\nWould you like to compare returns with another portfolio? (yes/no): ").strip().lower()

        if compare_another == "yes":  #If "yes", repeat the portfolio selection process
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
            daily_returns_dict2 = get_daily_returns(portfolio_percentages_2, start_date)
            cumulative_returns_2 = calculate_weighted_cumulative_returns(daily_returns_dict2, portfolio_percentages_2)
            break  #Exit the loop

        elif compare_another == "no":  #If "no", exit the process
            break

        else:  #If wrong input provided print error message and go back to beginning of loop
            print("\nInvalid input. Please choose \"yes\" or \"no\".")
            continue

    #Plotting the second cumulative returns in the same graph, if compare_another == "yes"
    if not cumulative_returns.empty and 'cumulative_returns_2' in locals() and not cumulative_returns_2.empty:
        plt.figure(figsize=(10, 6))
        cumulative_returns.plot(label=f'{portfolio_name}')
        cumulative_returns_2.plot(label=f'{portfolio_name_2}')
        plt.title("Comparison of Portfolio Performances Over Time")
        plt.xlabel("Date")
        plt.ylabel("Cumulative Returns")
        plt.legend()
        plt.gca().yaxis.grid(True)
        plt.gca().xaxis.grid(False)
        plt.show()

    #Delete the csv file for saving daily returns data
    os.remove("saved_daily_return_data.csv")

if __name__ == "__main__":
    main()