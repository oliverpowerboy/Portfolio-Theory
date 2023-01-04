import math

import numpy as np
import pandas as pd
from plotly import express as px


def co_variance(a, b):
    return 0.01


def portfolio_expected_return(*args):
    # this allows a tuple to be passed as an argument
    if len(args) == 1 and isinstance(args, tuple):
        args = args[0]

    list_of_expected_returns = [stock["weight"] * stock["expected_Return"] for stock in args]

    return sum(list_of_expected_returns)


def create_standard_deviation():
    pass


def portfolio_variance(*args, co_variance_table):
    # this allows a tuple to be passed as an argument
    if len(args) == 1 and isinstance(args, tuple):
        args = args[0]

    risk_of_securities = sum([((stock["weight"]) ** 2) * (stock["std_dev"]) for stock in args])

    diversification = []

    for stockA in args:
        for stockB in args:
            if stockA is stockB:
                continue
            else:
                diversification.append(2 * (stockA["weight"]) * (stockB["weight"])
                                       * co_variance_table[stockA["ticker"]][stockB["ticker"]])

    return risk_of_securities + sum(diversification)


def assign_random_weights(*portfolio, round_to_decimal=4):
    # Assigns random weights to securities in a portfolio, portfolio is 100% invested into securities
    # creating weights randomly is faster than creating every permutation of it

    # this allows a tuple to be passed as an argument
    if len(portfolio) == 1 and isinstance(portfolio, tuple):
        portfolio = portfolio[0]

    # Generates a matrix of random weights
    weights = np.random.random(len(portfolio))
    weights /= np.sum(weights)

    weights_applied_to_portfolios = []
    for index, stock in enumerate(portfolio):
        stock["weight"] = np.round(weights[index], round_to_decimal)
        weights_applied_to_portfolios.append(stock)

    return weights_applied_to_portfolios


def calculate_portfolio(portfolio, co_variance_table, round_to_decimal=4):
    variance_of_portfolio = round(math.sqrt(portfolio_variance(portfolio, co_variance_table=co_variance_table)),
                                  round_to_decimal)
    expected_return = round(portfolio_expected_return(portfolio), round_to_decimal)

    portfolio_dict = {"risk": variance_of_portfolio, "return": expected_return}

    for stock in portfolio:
        portfolio_dict[stock['ticker']] = stock['weight']

    return portfolio_dict


def global_min_max_return(dataframe):
    global_min_filter = (dataframe["risk"] == dataframe["risk"].min())
    global_min = dataframe[global_min_filter]

    global_min_max_return_filter = global_min["return"] == global_min["return"].max()
    global_min_max_return = global_min[global_min_max_return_filter]

    return global_min_max_return


# main here as an example of how to use functions
def main():
    # Example stocks
    stock_a = {"ticker": "GOOG", "std_dev": 0.07, "expected_Return": 0.013}
    stock_b = {"ticker": "IBM", "std_dev": 0.06, "expected_Return": 0.015}
    stock_c = {"ticker": "APPL", "std_dev": 0.07, "expected_Return": 0.016}
    stock_d = {"ticker": "MSFT", "std_dev": 0.05, "expected_Return": 0.013}
    stock_e = {"ticker": "TSLA", "std_dev": 0.06, "expected_Return": 0.12}
    stock_f = {"ticker": "LMAO", "std_dev": 0.075, "expected_Return": 0.074}

    stock_list = stock_a, stock_b, stock_c, stock_d, stock_e, stock_f

    results = []
    for i in range(100_000):
        portfolio_weights = assign_random_weights(stock_list)
        portfolio_calculated = calculate_portfolio(portfolio_weights)
        results.append(portfolio_calculated)

    dataframe = pd.DataFrame(results)

    dataframe.to_csv("portfolio.csv", index_label="index")

    dataframe["sharpe_Ratio"] = (dataframe["return"] - 0.04) / dataframe["risk"]
    # dataframe = dataframe.loc[sharpe_Ratio_Filter]

    print(global_min_max_return(dataframe))

    px.scatter(dataframe, x="risk", y="return", hover_data=dataframe.columns).show()


if __name__ == "__main__":
    main()
