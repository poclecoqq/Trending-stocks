import argparse
import datetime
import pickle
import os

from app import sentiment_analysis
from app.tweets_handler.fetcher import get_analyst_tweets, get_market_tweets

saved_data_floder = os.path.join(os.path.dirname(os.path.abspath(__file__)),"saved_data") 
if not os.path.exists(saved_data_floder):
    os.makedirs(saved_data_floder)

def initialize_argparser():
    parser = argparse.ArgumentParser(prog="tweet-analysis", description="Analyse tweet")
    args = parser.parse_args()
    return args

def tweets_analysis(tweets):
    stocks_polarity = {}
    if not tweets:
        print("No tweet found")
    else:
        for tweet in tweets:
            p = sentiment_analysis.get_polarity(tweet["text"])
            if p:
                s = sentiment_analysis.get_subjectivity(tweet["text"])
                if not tweet["stock"] in stocks_polarity:
                    stocks_polarity[tweet["stock"]] = [(p,s)]
                else:
                    stocks_polarity[tweet["stock"]].append((p,s))
    return stocks_polarity

def stock_sentiment_analysis(tweets_analysis):
    result = {}
    # print(tweets_analysis)
    for stock in tweets_analysis.keys():
        tot_polarity = 0
        tot_subjectivity = 0
        elem_nb = len(tweets_analysis[stock])
        for sa in tweets_analysis[stock]:
            tot_polarity = sa[0]
            tot_subjectivity = sa[1]
        result[stock] = (tot_polarity/elem_nb, tot_subjectivity/elem_nb)
    return result

def get_best_stocks(stock_sentiment, stock_number=10):
    a = stock_sentiment.items()
    # print(stock_sentiment)
    # print(a)
    return sorted(a,key=lambda x:x[1][0])

def save_data(tweets, filename="saved_data"):
    file_path = os.path.join(saved_data_floder,filename)
    with open(file_path, "wb") as file:
        pickle.dump(tweets, file)

def get_saved_data(filename="saved_data"):
    tweets = []
    file_path = os.path.join(saved_data_floder,filename)
    with open(file_path, "rb") as file:
        tweets = pickle.load(file)
    return tweets

if __name__ == "__main__":
    command_line_args = initialize_argparser()
    startDate = datetime.datetime(2019, 1, 1, 0, 0, 0)
    endDate =   datetime.datetime(2019, 2, 1, 0, 0, 0)


    tweets = get_analyst_tweets(startDate.strftime("%Y-%m-%d"), endDate.strftime("%Y-%m-%d"))
    tweets.extend(get_market_tweets(startDate.strftime("%Y-%m-%d"), endDate.strftime("%Y-%m-%d")))
    save_data(tweets, "tweets")
    # tweets = get_saved_data("tweets")
    tweets_sentiment = tweets_analysis(tweets)
    save_data(tweets_sentiment, "tweets_sentiment")
    stock_sentiment = stock_sentiment_analysis(tweets_sentiment)
    save_data(stock_sentiment, "stock_sentiment")
    print(stock_sentiment)
    best_stocks = get_best_stocks(stock_sentiment)
    print(best_stocks)
    save_data(best_stocks, "best_stocks")
    
