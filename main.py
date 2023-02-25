import pandas as pd
from plotly import express as px
import portfolio
import stock_data_creation as stock_create
import os

pd.options.display.width = 0

# Manually set
list_of_tickers = ("AAPL", "MSFT", "GOOG", "AMZN", "DAL", "ONEW", "GME", "ATVI")

# Creation of csv files of tickers, only needs to be if list_of_tickers is updated
# for ticker in list_of_tickers:
#     data = stock_create.get_ticker(ticker)
#     stock_create.save_ticker_data(data, ticker)

# Creation of stock objects

stock_object_array = [stock_create.stock(ticker) for ticker in list_of_tickers]
        

# stock_dicts = [stock_create.load_csv(stock) for stock in list_of_tickers]
# stock_dicts = [stock_create.expected_return_on_security(stock) for stock in stock_dicts]
# stock_dicts = [stock_create.std_dev_to_stock(stock) for stock in stock_dicts]

# Covariance table
corr_table = stock_create.correlation_table(stock_object_array)

print(corr_table)

# Creation of portfolios The larger the number inside of range() is the more likely the program will find the most
# efficient portfolio at the cost of processing power, however saving the best result each time will be equivalent as
# putting in a higher number
"""
portfolios = []

portfolio_limit = 100_000
for i in range(portfolio_limit):
    portfolio_weights = portfolio.assign_random_weights(stock_dicts)
    portfolio_calculated = portfolio.calculate_portfolio(portfolio_weights, corr_table)
    portfolios.append(portfolio_calculated)

    print(f"{i} portfolios calculated: {i/portfolio_limit}% completed",flush=True)

portfolio_dataframe = pd.DataFrame(portfolios)

print(portfolio.global_min_max_return(portfolio_dataframe))

px.scatter(portfolio_dataframe, x="risk", y="return", hover_data=portfolio_dataframe.columns).show()
"""