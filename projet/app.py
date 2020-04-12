from app.main import main
import argparse
import datetime


def initialize_argparser():
    parser = argparse.ArgumentParser(prog="tweet-analysis", description="Analyse tweet")
    today = datetime.date.today()
    parser.add_argument("-y", "--year", action="store", default=today.strftime("%Y"), help="Year for stock analysis")
    parser.add_argument("-m", "--month", action="store", default=today.strftime("%m"), help="Month for stock analysis")
    parser.add_argument("-d", "--day", action="store", default=today.strftime("%d"), help="Day for stock analysis")
    parser.add_argument("-p", "--period", action="store", default=30, help="Time period considered for stock analysis. Unit:days")
    parser.add_argument("-s", "--step", help="Execute program from which step. 1:Fetch stocks, 2:Fetch Twitter 3:Sentiment anlaysis", choices=["1", "2", "3"], default="1")
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
    print(end_date)
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

def get_step(args):
    return int(args.step)

def read_arguments(args):
    is_year_valid(args)
    is_period_valid(args)    
    start_date, end_date = build_period_dates(args)
    step = get_step(args)
    return start_date, end_date, step

def give_results(best_stocks):
    print("The best stocks are: ")
    for stock in best_stocks:
        print(stock, end = ', ')
    with open("output.txt", "w") as file:
        for stock in best_stocks:
            file.write(stock + ", ")


args = initialize_argparser()
start_date, end_date, step = read_arguments(args)
best_stocks = main(start_date, end_date, step)
give_results(best_stocks)