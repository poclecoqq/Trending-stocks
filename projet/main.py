import argparse
import datetime

from app import sentiment_analysis
from app.tweets_handler.fetcher import get_analyst_tweets, get_market_tweets

def initialize_argparser():
    parser = argparse.ArgumentParser(prog="tweet-analysis", description="Analyse tweet")
    # parser.add_argument("--user", type=str, help= "twitter username", required=True)
    args = parser.parse_args()
    return args



if __name__ == "__main__":
    # startDate = datetime.datetime(2019, 1, 1, 0, 0, 0)
    # endDate =   datetime.datetime(2019, 2, 1, 0, 0, 0)

    # print(get_analyst_tweets(startDate.strftime("%Y-%m-%d"), endDate.strftime("%Y-%m-%d")))
    command_line_args = initialize_argparser()
    startDate = datetime.datetime(2019, 1, 1, 0, 0, 0)
    endDate =   datetime.datetime(2019, 2, 1, 0, 0, 0)


    t = get_analyst_tweets(startDate.strftime("%Y-%m-%d"), endDate.strftime("%Y-%m-%d"))
    print(t)
    t.extend(get_market_tweets(startDate.strftime("%Y-%m-%d"), endDate.strftime("%Y-%m-%d")))
    print(t)
    if not t:
        print("No tweet found")
    for tweet in t:
        p = sentiment_analysis.get_polarity(tweet["text"])
        s = sentiment_analysis.get_subjectivity(tweet["text"])
        print(u"Polarity {}, subjectivity {}".format(p, s))
    
