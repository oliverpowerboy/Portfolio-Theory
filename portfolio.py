import stock_data_creation as stock_creation
import numpy as np


def global_min_max_return(dataframe):
    global_min_filter = (dataframe["risk"] == dataframe["risk"].min())
    global_min = dataframe[global_min_filter]

    global_min_max_return_filter = global_min["return"] == global_min["return"].max()
    global_min_max_return = global_min[global_min_max_return_filter]

    return global_min_max_return


def risk(weights, corrolation_table):
    return np.sqrt(np.dot(weights.T, np.dot(corrolation_table, weights))) * np.sqrt(252)


def expected_return(securities,weights):
    returns = (np.array([i.expected_return for i in securities]))
    # 252 as it is daily returns
    return np.dot(returns, weights) * 252


def create_weights(number_of_securities,invested_percent=1):
    weights = np.random.random(number_of_securities)
    return weights / (np.sum(weights) * invested_percent)


class portfolioObject():
    count = 0

    def __init__(self,stocks, weight=None, corrolation_table=None):

        portfolioObject.count += 1

        self.stocks = stocks

        self.tickers = [s.ticker for s in stocks]

        if weight is None:
            self.weight = create_weights(len(stocks))
        else:
            self.weight = weight

        if corrolation_table is None:
            self.corrolation_table = stock_creation.correlation_table(stocks)
        else:
            self.corrolation_table = corrolation_table

        self.expected_return = expected_return(self.stocks, self.weight)

        self.risk = risk(self.weight, corrolation_table)


