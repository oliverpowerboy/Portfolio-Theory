import yfinance as yf
import pandas as pd
import os
import numpy as np
import plotly.express as px


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

    # if not "cumulative_return" in ticker_data.columns:
    #     add_cumulative_returns(ticker_data)

    ticker_data.to_csv(os.path.join(path, ticker + ".csv"))


# correlation of change in stock price between assets
def correlation_table(portfolio):
    def merge_columns(cols, securities):
        df = pd.DataFrame()

        for security in securities:
            df[security.ticker] = security.data[cols]

        return df

    data = merge_columns("Close",portfolio)
    returns = np.log(data / data.shift(1))

    return returns.cov()

class stock:
    path = "securities"
    def __init__(self, ticker, data=None) -> None:
        self.ticker = ticker

        if data is None:
            self.data = pd.read_csv(os.path.join(stock.path, self.ticker + ".csv"))
        else:
            self.data = data

    @property
    def expected_return(self):
        return (self.data["Close"] + self.data["Dividends"].cumsum()).pct_change().mean()

    @property
    def standard_deviation(self):

        returns = np.log(self.data["Close"] / self.data["Close"].shift(1))
        return  returns.std()

    def __repr__(self):
        return f"stock({self.ticker, self.data.head(5)}\n)"