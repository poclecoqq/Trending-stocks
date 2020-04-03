import os 
import csv
import datetime
from queue import Queue
from threading import Thread
from threading import Lock

from communications import get_tweets

c_dir = os.path.dirname(os.path.realpath(__file__))
gtweets_loc = Lock()
gtweets = []


class TweetsWorker(Thread):

    def __init__(self, input_queue, id):
        Thread.__init__(self)
        self.input_queue = input_queue
        self.id = id

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            start_date, end_date, querry_filter, user = self.input_queue.get()
            try:
                print("get tweets thread running")
                t = get_tweets(username=user, start_date=start_date,end_date=end_date,query_search=querry_filter, toptweets=True, maxtweets=1, got_output_file=str(self.id) + ".csv" )
                gtweets_loc.acquire()
                gtweets.extend(t)
                gtweets_loc.release()
            finally:
                self.input_queue.task_done()


def start_querries(querries):
    gtweets = []
    # Create a queue to communicate with the worker threads
    task_queue = Queue()
    # Create 8 worker threads
    for i in range(8):
        worker = TweetsWorker(task_queue, i)
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()
    # Put the tasks into the queue as a tuple
    for querry in querries:
        task_queue.put(querry)
    # Causes the main thread to wait for the queue to finish processing all the tasks
    task_queue.join()

    return gtweets



def get_finance_twitter_accounts():
    fin_csv = os.path.join(c_dir, "data", "finance_accounts.csv")
    accounts = []
    with open(fin_csv, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            accounts.append(row[0])
    return accounts


def valid_row(row):
    complete_row = True
    for elem in row:
        if not elem:
            complete_row = False
    return complete_row

def get_cached_stocks():
    fin_csv = os.path.join(c_dir, "data", "test.csv")
    stocks = []
    with open(fin_csv, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if valid_row(row):
                stocks.append((row[0],row[1],row[2]))
    return stocks



def get_analyst_tweets(start_date, end_date, stocks=None):
    twitter_accounts = get_finance_twitter_accounts()
    if not stocks:
        stocks = get_cached_stocks()
    tweets = {}
    for stock in stocks:
        # the ticker is the key
        tweets[stock[1]] = []
        # add every tweet betweem start and end date concerning the stock
        for analyst in twitter_accounts:
            querry_filter = str(stock[1]) + " " + str(stock[2])
            tweets[stock[1]].extend(get_tweets(analyst, start_date, end_date, querry_filter))
    return tweets
    

def get_market_tweets(start_date, end_date, stocks=None):
    if not stocks:
        stocks = get_cached_stocks()
    start_querries([ (start_date, end_date, str(stock[0]) + " " + str(stock[1]) + " stock market", None) for stock in stocks])

if __name__ == "__main__":
    startDate = datetime.datetime(2019, 1, 1, 0, 0, 0)
    endDate =   datetime.datetime(2019, 2, 1, 0, 0, 0)

    print(get_market_tweets(startDate.strftime("%Y-%m-%d"), endDate.strftime("%Y-%m-%d")))