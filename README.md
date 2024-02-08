# Crypto Portfolio Analysis Tool

## Table of Contents
- [Installation](#installation)
- [Description](#description)
- [Usage](#usage)
- [Next Steps](#future-work)

## Installation
- Ensure you have Python installed on your system.
- Clone this repository to your local machine.
- Navigate to the project directory and install dependencies using `pip install -r requirements.txt`.
- An API key from CoinMarketCap is required for accessing cryptocurrency data. The default API key provided in `config.ini` is ours, but we encourage you to obtain your own key from [coinmarketcap.com](https://coinmarketcap.com/api/) for free.

## Description
This tool is designed to analyze cryptocurrency portfolios using data from CoinMarketCap and Yahoo Finance. It provides functionalities to calculate and visualize different types of portfolios based on live market capitalization, equal weighting, or global minimum variance. The main features include:
- Listing all available cryptocurrency slugs using CoinMarketCap's API.
- Calculating three types of portfolios: Value Weighted, Equal Weighted, and Global Minimum Variance.
- Visualizing portfolio percentages with a pie chart.
- Comparing portfolio returns over a specified time period.


## Usage
To use the tool, run `main.py` from the command line with the following options:
- `--list` to display all available cryptocurrency slugs.
- Without parameters to use interactive mode for portfolio selection and comparison.

Example command:
```bash

python main.py

```

You will be prompted to:
1. Enter up to 5 cryptocurrency slugs or choose "top3"/"top5" by market cap. You can also type "list" to list all available slugs.
2. Enter a time period for analysis (e.g., "5D" for 5 days, "1W" for 1 week, "6M" for 6 months, "1Y" for 1 year). The default period is 1 month.
3. Choose a portfolio type (Value Weighted, Equal Weighted, Global Minimum Variance).

After making your selections, the tool will generate and display a pie chart of the portfolio percentages. Following this, it will show charts of portfolio returns and allow you to compare returns with another chosen portfolio type.

Another Example command:
```bash

python main.py --list

```
This will list all available cryptocurrency slugs

## Next Steps
Future enhancements may include:
- Integration of additional data sources for more comprehensive analysis.
- Expansion of the portfolio types and comparison metrics.
- Improvement of the visualization features to offer more customization options.
- Optimization of API usage to enhance performance and reduce data retrieval times.

## Authors: Sebastian Pasz and Tomáš Šamaj