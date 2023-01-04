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


def merge_columns(cols, *securities):

    # this allows a tuple to be passed as an argument
    if len(securities) == 1 and isinstance(securities, tuple):
        securities = securities[0]

    df = pd.DataFrame()

    for security in securities:
        df[security["ticker"]] = security["data"][cols]

    return df


def expected_return_on_security(stock):

    returns = np.log(stock["data"]["Close"] / stock["data"]["Close"].shift(1))

    # 252 trading days in a year
    stock["expected_Return"] = returns.mean() * 252

    return stock

# correlation of change in stock price between assets
def correlation_table(portfolio):

    data = merge_columns("Close",portfolio)
    returns = np.log(data / data.shift(1))

    return returns.cov()

def std_dev_to_stock(stock):

    returns = np.log(stock["data"]["Close"] / stock["data"]["Close"].shift(1))
    stock["std_dev"] = returns.std()

    return stock
