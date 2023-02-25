import yfinance as yf
import pandas as pd
import os
import numpy as np


# get ticker data
def get_ticker(ticker, period="5y", interval="1d"):

    ticker = yf.Ticker(ticker)
    history = ticker.history(period=period, interval=interval)

    return history


# daily returns
def add_period_returns(dataframe):

    dataframe["daily_return"] = (dataframe["Close"] / dataframe["Close"].shift(1)) - 1

    return dataframe


# cumulative returns
def add_cumulative_returns(dataframe):

    if not "daily_return" in dataframe.columns:
        add_period_returns(dataframe)

    dataframe["cumulative_return"] = (1 + dataframe["daily_return"]).cumprod()

    return dataframe


# store to csv
def save_ticker_data(ticker_data, ticker, path="securities"):

    if not os.path.exists(path):
        os.makedirs(path)

    if not "cumulative_return" in ticker_data.columns:
        add_cumulative_returns(ticker_data)

    ticker_data.to_csv(os.path.join(path, ticker + ".csv"))


def load_csv(ticker, path="securities"):
    path = os.path.join(path, ticker + ".csv")
    return {"ticker": ticker,
            "data": pd.read_csv(filepath_or_buffer=path, index_col="Date")}


def merge_columns(cols, securities):

    df = pd.DataFrame()

    for security in securities:
        df[security.ticker] = security.data[cols]

    return df


def expected_return_on_security(data):
    # Changed from stock dict to dataframe

    returns = np.log(data["Close"] / data["Close"].shift(1))

    # 252 trading days in a year
    data["expected_Return"] = returns.mean() * 252

    return data

# correlation of change in stock price between assets
def correlation_table(portfolio):

    data = merge_columns("Close",portfolio)
    returns = np.log(data / data.shift(1))

    return returns.cov()

def std_dev_to_stock(data):

    # Changed from stock dict to dataframe

    returns = np.log(data["Close"] / data["Close"].shift(1))
    data["std_dev"] = returns.std()

    return data

class stock:
    path = "securities"
    def __init__(self, ticker, data=None) -> None:
        self.ticker = ticker

        if data is None:
            self.data = pd.read_csv(os.path.join(stock.path, self.ticker + ".csv"))
        else:
            self.data = data

        self.returns = expected_return_on_security(self.data)

        self.standard_deviation = std_dev_to_stock(self.data)