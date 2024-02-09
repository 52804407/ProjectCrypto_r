# Crypto Portfolio Returns Analysis Tool

## Table of Contents
- [Installation](#installation)
- [Description](#description)
- [Usage](#usage)
- [Potential Future Improvements](#potential-future-improvements-wish-list)

## Installation
- Ensure you have the correct version of Python (specified in `requirements.txt` ) installed.
- Clone this repository to your local machine.
- Navigate to the project directory and install dependencies using `pip install -r requirements.txt`.
- An API key from CoinMarketCap is required for accessing cryptocurrency market capitalization data (for the value-weighted portfolio setting). The default API key provided in `config.ini` is ours, but we encourage you to obtain your own key from [coinmarketcap.com](https://coinmarketcap.com/api/) for free.

## Description
This tool is designed to analyze returns of cryptocurrency portfolios using data from [CoinMarketCap](https://coinmarketcap.com/api/) and [Yahoo Finance](https://pypi.org/project/yfinance/) APIs. It provides functionalities to calculate and visualize different types of portfolios (Value-Weighted, Equal-Weighted, and Global Minimum Variance). 

The main features include:
- **Specifying a portfolio** of user's choice (maximum of 5 currencies) or listing all available cryptocurrency slugs (TOP 50 cryptocurrencies by market cap).
- **Choosing a time period** for the portfolio returns analysis (end date is set as `today`, i.e. the day on which the code is executed).
- **Calculating three types of portfolios**: Value-Weighted (based on live market caps), Equal-Weighted, and Global Minimum Variance (with an initial guess of equal weights).<br>
_Note: As the covariance of various cryptocurrencies is very low in some portfolios, the GMV portfolio might yield equal weights, as it is the initial guess in the variance optimization process._
- **Visualizing portfolio percentages** distributions in a pie chart.
- **Visualizing cumulative portfolio returns** over time in a plot.
- **Comparing returns** of different portfolio types over a specified time period.<br>
_Note: Here we implement a data saving process to reduce runtime by preventing downloading the same data twice. Daily return data are saved in a temporary csv file._



## Usage
To use the tool, run `main.py` from the command line with the following options:
- Without parameters to use interactive mode for portfolio selection and comparison.

Example command:
```bash

python main.py

```

The user will be prompted to:
1. Enter up to 5 cryptocurrency slugs or choose "top3"/"top5" by market cap. You can also type "list" to list all available slugs.
2. Enter a time period for analysis (e.g., "5D" for 5 days, "1W" for 1 week, "6M" for 6 months, "1Y" for 1 year). The default period is 1 month. The maximum period lenght is set to 3 years.
3. Choose a portfolio type (Value-Weighted, Equal-Weighted, Global Minimum Variance).

After making the selections, the tool will generate and display a pie chart of the portfolio percentages. Following this, it will plot portfolio returns and allow the user to compare returns with another chosen portfolio type.




## Potential Future Improvements (Wish List)
Future enhancements of our project might include:
- Add more portfolio types and extend the list of cryptocurrency slugs.
- Further improve the data saving process across different runs of `main.py` to further reduce runtime by preventing downloads of overlapping data.
- Add periodic portfolio rebalancing (e.g. every 2 weeks). For this, historical values of market caps are crucial. However, the free version of CoinMarketCap API provides only live data.
- Optimization of API usage to reduce data retrieval times.

**Authors: Sebastian Pasz and Tomáš Šamaj**