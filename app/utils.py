import os
import pickle
import csv

c_dir = os.path.dirname(os.path.abspath(__file__))
prototype_data_folder = os.path.join(c_dir, "prototype_data")
saved_data_floder = os.path.join(c_dir,"saved_data") 
if not os.path.exists(saved_data_floder):
    os.makedirs(saved_data_floder)

def save_data(tweets, filename="tweets"):
    file_path = os.path.join(saved_data_floder,filename)
    with open(file_path, "wb") as file:
        pickle.dump(tweets, file)

def get_saved_data(filename="tweets"):
    tweets = []
    file_path = os.path.join(saved_data_floder,filename)
    with open(file_path, "rb") as file:
        tweets = pickle.load(file)
    return tweets


def get_prototype_stocks():
    fin_csv = os.path.join(prototype_data_folder, "long_companies.csv")
    stocks = []
    with open(fin_csv, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if valid_row(row):
                stocks.append((row[0],row[1],row[2]))
    return stocks

def valid_row(row):
    complete_row = True
    for elem in row:
        if not elem:
            complete_row = False
    return complete_row