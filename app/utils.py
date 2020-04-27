import os
import pickle
import csv

c_dir = os.path.dirname(os.path.abspath(__file__))


def valid_row(row):
    return row[0] and row[1]


def read_stock_file(path_to_file):
    fin_csv = os.path.join(path_to_file)
    stocks = []
    with open(fin_csv, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if valid_row(row):
                stocks.append((row[0],row[1]))
    return stocks