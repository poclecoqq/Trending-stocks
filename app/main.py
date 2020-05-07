import datetime

from . import sentiment_analysis
from .tweets_handler.fetcher import get_analyst_tweets, get_market_tweets
from . import utils

def querry_twitter(startDate, endDate, stocks):
    tweets = get_analyst_tweets(startDate, endDate, stocks)
    tweets.extend(get_market_tweets(startDate, endDate, stocks))
    return tweets

def get_best_stocks(tweets, stock_number=10):
    stock_sentiment = sentiment_analysis.get_stock_sentiment(tweets)
    sorted_stocks = sorted(stock_sentiment.items(),key=lambda x:x[1][0], reverse=True)[:stock_number]
    return [x[0] for x in sorted_stocks]

def main(startDate, endDate, stocks):
    tweets = querry_twitter(startDate, endDate, stocks)
    best_stocks = get_best_stocks(tweets)
    return best_stocks
    
    
    
