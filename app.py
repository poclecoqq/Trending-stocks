from app.main import main
from app import utils
import argparse
import datetime
import app.tweets_handler.fetcher as fetcher

def initialize_argparser():
    parser = argparse.ArgumentParser(prog="tweet-analysis", description="Analyse tweet. See README file for more details.")
    today = datetime.date.today()
    parser.add_argument("-f", "--file", action="store", help="Path to file containing stocks", metavar="PATH")
    parser.add_argument("-y", "--year", action="store", default=today.strftime("%Y"), help="Year for stock analysis", metavar="[2007-today]")
    parser.add_argument("-m", "--month", action="store", default=today.strftime("%m"), help="Month for stock analysis", metavar="[1-12]")
    parser.add_argument("-d", "--day", action="store", default=today.strftime("%d"), help="Day for stock analysis", metavar="[0-31]")
    parser.add_argument("-p", "--period", action="store", default=30, help="Time period considered for stock analysis. Unit:days", metavar="DAYS")
    parser.add_argument("-t", "--thread", help="Computationnal ressources used for queerying twitter. ", choices=[str(i) for i in range(1,101)], default=2, metavar="[0-100]")
    args = parser.parse_args()
    return args

def is_year_valid(args):
    year = int(args.year)
    # Can't search before Twitter was created
    if year < 2007: 
        exit("Year must be higher than 2007")

def is_period_valid(args):
    period = int(args.period)
    if period:
        if period <= 0:
            exit("Period must be a number bigger than zero! Exiting.")



def build_period_dates(args):
    period = datetime.timedelta(int(args.period))
    end_date = args.year + "-" + args.month + "-" + args.day 
    try:
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    except:
        exit("Given date does not exists. Exiting.")
    if end_date > datetime.datetime.today():
        exit("Search period must be before today. Given date: {0}".format(end_date.strftime("%Y-%m-%d")))
    start_date =  end_date - period
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    return start_date, end_date

def get_stocks(args):
    file_path = str(args.file)
    if not utils.file_exists(file_path):
        file_path = "./tsx_1B.csv"
    return utils.read_stock_file(file_path)

def read_arguments(args):
    is_year_valid(args)
    is_period_valid(args)    
    start_date, end_date = build_period_dates(args)
    stocks = get_stocks(args)
    return start_date, end_date, stocks

def output_results(best_stocks):
    print("The best stocks are: ", end = '')
    print(", ".join(best_stocks))
    print()
    with open("output.txt", "w") as file:
        for stock in best_stocks:
            file.write(stock + ", ")

def set_thread_number(args):
    threads = int(args.thread)
    fetcher.thread_nb = threads

args = initialize_argparser()
set_thread_number(args)
start_date, end_date, stocks = read_arguments(args)
best_stocks = main(start_date, end_date, stocks)
output_results(best_stocks)