from datetime import datetime
from dateutil.relativedelta import relativedelta

def read_results(file_path: str):
    dateformat = "%Y-%m-%d"
    file = open(file_path, "r")
    results = {}
    date = datetime.strptime("2020-01-01", dateformat)
    for line in file:
        stocks = line.strip().split()
        results[date.strftime(dateformat)] = stocks
        date = date - relativedelta(months=3)
    return results


print(read_results("./res.txt"))