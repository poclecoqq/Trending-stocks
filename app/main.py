import datetime

from . import sentiment_analysis
from .tweets_handler.fetcher import get_analyst_tweets, get_market_tweets
from . import utils


def tweets_analysis(tweets):
    stocks_polarity = {}
    if not tweets:
        exit("No tweet found")
    else:
        for tweet in tweets:
            p = sentiment_analysis.get_polarity(tweet["text"])
            if p:
                s = sentiment_analysis.get_subjectivity(tweet["text"])
                if not tweet["stock"] in stocks_polarity:
                    stocks_polarity[tweet["stock"]] = [(p,s)]
                else:
                    stocks_polarity[tweet["stock"]].append((p,s))
    if not stocks_polarity:
        exit("Could not extract polarity from given tweets. Program finished.")
    return stocks_polarity

def stock_sentiment_analysis(tweets_analysis):
    result = {}
    for stock in tweets_analysis.keys():
        tot_polarity = 0
        tot_subjectivity = 0
        elem_nb = len(tweets_analysis[stock])
        for sa in tweets_analysis[stock]:
            tot_polarity = sa[0]
            tot_subjectivity = sa[1]
        result[stock] = (tot_polarity/elem_nb, tot_subjectivity/elem_nb)
    return result

def top_stocks(stock_sentiment, stock_number=10):
    a = stock_sentiment.items()
    return sorted(a,key=lambda x:x[1][0], reverse=True)[:stock_number]


def querry_twitter(startDate, endDate, stocks):
    tweets = get_analyst_tweets(startDate, endDate, stocks)
    tweets.extend(get_market_tweets(startDate, endDate, stocks))
    return tweets

def get_best_stocks(tweets):
    tweets_sentiment = tweets_analysis(tweets)
    stock_sentiment = stock_sentiment_analysis(tweets_sentiment)
    return top_stocks(stock_sentiment)


def main(startDate, endDate, path_to_file):
    stocks = utils.read_stock_file(path_to_file)
    tweets = querry_twitter(startDate, endDate, stocks)
    best_stocks = get_best_stocks(tweets)
    return [x[0] for x in best_stocks]
    
    
    
