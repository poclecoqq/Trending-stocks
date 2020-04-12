import os 
import csv
import datetime
from queue import Queue
from threading import Thread
from threading import Lock

from .communications import get_tweets

c_dir = os.path.dirname(os.path.realpath(__file__))
gtweets_loc = Lock()
gtweets = []
thread_nb = 2

def add_tweets(stock, tweets):
    for tweet in tweets:
        tweet["stock"] = stock
    global gtweets, gtweets_loc
    gtweets_loc.acquire()
    gtweets.extend(tweets)
    gtweets_loc.release()

class TweetsWorker(Thread):

    def __init__(self, input_queue, id):
        Thread.__init__(self)
        self.input_queue = input_queue
        self.id = id

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            start_date, end_date, querry_filter, stock, user  = self.input_queue.get()
            print("Querrying for stock: ", stock)
            try:
                t = get_tweets(username=user, start_date=start_date,end_date=end_date,query_search=querry_filter, maxtweets=100, got_output_file=str(self.id) + ".csv" )
                add_tweets(stock, t)
            finally:
                self.input_queue.task_done()


def start_querries(querries):
    global gtweets, thread_nb
    gtweets = []
    # Create a queue to communicate with the worker threads
    task_queue = Queue()
    # Create worker threads
    for i in range(thread_nb):
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


# make market tweets about stock filter    
def make_analyst_filter(stock):
    return str(stock[0]) + " " + str(stock[1])

def get_analyst_tweets(start_date, end_date, stocks):
    print("Fetching analyst tweets")
    twitter_accounts = get_finance_twitter_accounts()
    return start_querries([ (start_date, end_date, make_analyst_filter(stock), stock[1], user) for stock in stocks for user in twitter_accounts])

# make market tweets about stock filter    
def make_market_filter(stock):
    return str(stock[0]) + " " + str(stock[1]) + " stock market"

def get_market_tweets(start_date, end_date, stocks):
    print("Fetching market tweets")
    return start_querries([ (start_date, end_date, make_market_filter(stock), stock[1], None) for stock in stocks])

if __name__ == "__main__":
    startDate = datetime.datetime(2017, 1, 1, 0, 0, 0)
    endDate =   datetime.datetime(2019, 2, 1, 0, 0, 0)

    print(get_market_tweets(startDate.strftime("%Y-%m-%d"), endDate.strftime("%Y-%m-%d")))
