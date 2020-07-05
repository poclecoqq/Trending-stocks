import os
import sys
from datetime import datetime
import pickle

import yfinance as yf
from dateutil.relativedelta import relativedelta

from utils import list_average, read_results, plot_yields, to_valid_open_market_day


output = sys.stdout
to_null = open(os.devnull, 'w')


def get_3_month_yield(ticker: str, date: str):
    stock_value = request_stock(ticker, date)
    stock_yield = (stock_value.iloc[-1]["Close"] -
                   stock_value.iloc[0]["Close"]) / stock_value.iloc[0]["Close"]
    return 1 + stock_yield


def request_stock(ticker_name: str, date: str):
    sys.stdout = to_null
    ticker_name = special_cases(ticker_name)
    if "." in ticker_name:
        ticker_name = ticker_name.replace(".", "-")
    ticker = yf.Ticker(ticker_name)
    stock_value = ticker.history(start=date, period="3mo")
    if stock_value.empty:
        ticker = yf.Ticker(ticker_name + ".TO")
        stock_value = ticker.history(start=date, period="3mo")
    sys.stdout = output
    return stock_value


def special_cases(ticker_name: str):
    if ticker_name == "BYD.UN":
        ticker_name = "BYD"
    elif ticker_name == "FCR":
        ticker_name = "FCR-UN"
    return ticker_name


def get_stocks_yields(stocks, date):
    yields = []
    for stock in stocks:
        if stock in ["MDA", "PWT", "DDC", "POT", "MST.UN", "AYA", "DRG.UN", "PHY.U", "VRX", "SLW"]:
            continue
        stock_yield = get_3_month_yield(stock, date)
        yields.append(stock_yield)
    return yields


def average_yields(stocks):
    total_yield = {}
    for date in results:
        yields = get_stocks_yields(results[date], date)
        average_yield = list_average(yields)
        total_yield[date] = average_yield
    return total_yield


# results = read_results("./res.txt")
# y = average_yields(results)
# print(y)

index = yf.Ticker("^GSPTSE")
his = index.history(start="2009-12-01", end="2020-03-01")

start_value = his.iloc[0]['Close']
index_yield = {}
for index, row in his.iterrows():
    index_yield[index.to_pydatetime()] = row['Close'] / start_value

print(index_yield)
# f = open("a", "wb")
# pickle.dump(y, f)
f = open("b", "wb")
pickle.dump(index_yield, f)

f = open("a", "rb")
y = pickle.load(f)
# f = open("b", "rb")
# his = pickle.load(f)

plot_yields(y, index_yield)
