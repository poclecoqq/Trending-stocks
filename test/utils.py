import math
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import holidays

from dateutil.relativedelta import relativedelta
date_format = "%Y-%m-%d"


def df_to_yield_dic(df):
    global date_format
    start_value = df.iloc[0]['Close']
    yield_dic = {}
    for index, row in df.iterrows():
        yield_dic[index.to_pydatetime().strftime(
            date_format)] = row['Close'] / start_value
        start_value = row['Close']
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
    global date_format
    file = open(file_path, "r")
    results = {}
    date = datetime.strptime("2020-01-01", date_format)
    for line in file:
        stocks = line.replace(" ", "").replace("\n", "").split(",")
        results[date.strftime(date_format)] = stocks
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
    global date_format
    day = datetime.strptime(day, date_format)
    # if date is a weekend day or holiday, find closest week day
    while day.weekday() in [5, 6] or day in holidays.CA():
        day = day - timedelta(days=1)
    return day.strftime(date_format)


def date_sort(dic):  # Input: dictionnary with date as key. Ouput: list of keys sorted + list of values in the corresponding order
    global date_format
    dates = list(dic.keys())
    dates = sorted(dates, key=lambda key: datetime.strptime(
        key, date_format))  # asc date sort
    yields = [dic[date] for date in dates]
    return dates, yields


def compose_yield(yields):
    composed_yields = [yields[0]]
    for i in range(1, len(yields)):
        composed_yields.append(composed_yields[-1] * yields[i])
        print(composed_yields[-1],  yields[i])
    return composed_yields


def extract_yields(dates, date_list, yield_list):
    yields = []
    for date in dates:
        i = date_list.index(date)
        yields.append(yield_list[i])
    return yields


def prepare_data_for_plotting(stock_picked, index):
    dates, stock_picked_yields = date_sort(stock_picked)
    stock_picked_composed_yields = compose_yield(stock_picked_yields)
    index_dates, index_yields = date_sort(index)
    index_composed_yields = compose_yield(index_yields)
    valid_index_dates = [to_valid_open_market_day(date) for date in dates]
    index_composed_yields = extract_yields(
        valid_index_dates, index_dates, index_composed_yields)
    return dates, stock_picked_composed_yields, index_composed_yields


def plot_yields(stock_picked, index):  # TODO: Extraire une fonction de ]ca

    dates, stock_picked_composed_yields, index_composed_yields = prepare_data_for_plotting(
        stock_picked, index)
    plt.plot(dates, stock_picked_composed_yields, marker='o', markerfacecolor='blue',
             markersize=5, label="stock pick")
    plt.plot(dates, index_composed_yields, marker='o',
             markerfacecolor='red', markersize=5, label="GSPTSE")
    plt.legend()

    plt.xlabel("yield")
    plt.ylabel("date")
    plt.title("Stock pick vs index")

    plt.show()
