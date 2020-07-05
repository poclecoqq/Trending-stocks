import math
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import holidays

from dateutil.relativedelta import relativedelta


def df_to_yield_dic(df):
    start_value = df.iloc[0]['Close']
    yield_dic = {}
    for index, row in df.iterrows():
        yield_dic[index.to_pydatetime()] = row['Close'] / start_value
    return yield_dic


def find_first_close_value(df):
    val = 0
    i = 0
    while(not val and i < df.shape[0]):
        val = df.iloc[i]["Close"]
        i += 1
    return val


def find_last_close_value(df):
    val = 0
    i = df.shape[0] - 1
    while(not val and i >= 0):
        val = df.iloc[i]["Close"]
        i -= 1
    return val


def read_results(file_path: str):
    dateformat = "%Y-%m-%d"
    file = open(file_path, "r")
    results = {}
    date = datetime.strptime("2020-01-01", dateformat)
    for line in file:
        stocks = line.replace(" ", "").replace("\n", "").split(",")
        results[date.strftime(dateformat)] = stocks
        date = date - relativedelta(months=3)
    return results


def list_average(list_: []):
    nb = 0
    sum = 0
    for elem in list_:
        if elem and not math.isnan(elem):
            sum += elem
            nb += 1
    return sum / nb


def to_valid_open_market_day(day: str):
    day = datetime.strptime(day, "%Y-%m-%d")
    # if date is a weekend day or holiday, find closest week day
    while day.weekday() in [5, 6] or day in holidays.CA():
        day = day - timedelta(days=1)
    return day


def plot_yields(stock_picked, index):
    dates = list(stock_picked.keys())
    dates = sorted(dates, key=lambda pair: datetime.strptime(
        pair, "%Y-%m-%d"))
    result = [stock_picked[date] for date in dates]
    for i in range(1, len(result)):
        result[i] = result[i-1] * result[i]
    index_result = [
        index[to_valid_open_market_day(date)] for date in dates]
    plt.plot(dates, result, marker='o', markerfacecolor='blue',
             markersize=5, label="stock pick")
    plt.plot(dates, index_result, marker='o',
             markerfacecolor='red', markersize=5, label="GSPTSE")
    plt.legend()

    plt.xlabel("yield")
    plt.ylabel("date")
    plt.title("Stock pick vs index")

    plt.show()
