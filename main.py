import pandas as pd
from plotly import express as px
import portfolio
import stock_data_creation as stock_create

pd.options.display.width = 0

# Manually set
list_of_tickers = ("AAPL", "MSFT", "GOOG", "AMZN", "DAL", "ONEW", "GME", "ATVI")

# Creation of csv files of tickers, only needs to be if list_of_tickers is updated
# for ticker in list_of_tickers:
#     data = stock_create.get_ticker(ticker)
#     stock_create.save_ticker_data(data, ticker)

# Creation of stock objects
stock_dicts = [stock_create.load_csv(stock) for stock in list_of_tickers]
stock_dicts = [stock_create.expected_return_on_security(stock) for stock in stock_dicts]
stock_dicts = [stock_create.std_dev_to_stock(stock) for stock in stock_dicts]

# Covariance table
corr_table = stock_create.correlation_table(stock_dicts)

# Creation of portfolios The larger the number inside of range() is the more likely the program will find the most
# efficient portfolio at the cost of processing power, however saving the best result each time will be equivalent as
# putting in a higher number

portfolios = []
for i in range(100_000):
    portfolio_weights = portfolio.assign_random_weights(stock_dicts)
    portfolio_calculated = portfolio.calculate_portfolio(portfolio_weights, corr_table)
    portfolios.append(portfolio_calculated)

portfolio_dataframe = pd.DataFrame(portfolios)

print(portfolio.global_min_max_return(portfolio_dataframe))

px.scatter(portfolio_dataframe, x="risk", y="return", hover_data=portfolio_dataframe.columns).show()
