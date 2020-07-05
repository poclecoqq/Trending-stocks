import os
import sys
from datetime import datetime
import pickle

import yfinance as yf
from dateutil.relativedelta import relativedelta

import utils

output = sys.stdout
to_null = open(os.devnull, 'w')


def get_3_month_yield(ticker: str, date: str):
    stock_value = request_stock(ticker, date)
    start_value = utils.find_first_close_value(stock_value)
    end_value = utils.find_last_close_value(stock_value)
    stock_yield = (end_value - start_value) / start_value
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
        average_yield = utils.list_average(yields)
        total_yield[date] = average_yield
    return total_yield


results = utils.read_results("./res.txt")
y = average_yields(results)

index = yf.Ticker("^GSPTSE")
his = index.history(start="2009-12-01", end="2020-03-01")

index_yield = utils.df_to_yield_dic(his)

utils.plot_yields(y, index_yield)
