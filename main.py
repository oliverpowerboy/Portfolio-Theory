import pandas as pd
from plotly import express as px
import portfolio
import stock_data_creation as stock_create
import time
import concurrent.futures

# Creation of csv files of tickers, only needs to be if list_of_tickers is updated
# for ticker in list_of_tickers:
#     data = stock_create.get_ticker(ticker)
#     stock_create.save_ticker_data(data, ticker)

# Creation of stock objects


def generate_portfolio(securities, corr_table):

    x = portfolio.portfolioObject(securities, corrolation_table=corr_table)

    return_dict = {"return": x.expected_return, "risk": x.risk}

    for index, sec in enumerate(securities):
        return_dict[sec.ticker] = x.weight[index]

    result_frame = pd.DataFrame.from_dict([return_dict])

    return result_frame

if __name__ == "__main__":



    pd.options.display.width = 0
    # Manually set
    list_of_tickers = ("AAPL", "MSFT", "GOOG", "AMZN", "DAL")

    stock_object_array = [stock_create.stock(ticker) for ticker in list_of_tickers]

    # Covariance table
    corr_table = stock_create.correlation_table(stock_object_array)

    dataframe = pd.DataFrame()

    generate_count = 100_000

    start = time.perf_counter()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(generate_portfolio, stock_object_array, corr_table) for _ in range(generate_count)]

        for f in concurrent.futures.as_completed(futures):
            x = f.result()

            dataframe = pd.concat([dataframe, x])


    finish = time.perf_counter()

    print(f"Finished multiprocessing in {finish-start} seconds.") # Finished multiprocessing in 270.20366010000004 seconds.

    dataframe = pd.DataFrame()

    start = time.perf_counter()

    data = [generate_portfolio(stock_object_array, corr_table) for _ in range(generate_count)]

    dataframe = pd.concat([dataframe, pd.DataFrame([data])])

    finish = time.perf_counter()

    print(f"Finished non-multiprocessing in {finish - start} seconds.") # Finished non-multiprocessing in 223.4125871 seconds.

