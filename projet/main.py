import argparse
import datetime

from app import sentiment_analysis, tweets_handler

def initialize_argparser():
    parser = argparse.ArgumentParser(prog="tweet-analysis", description="Analyse tweet")
    parser.add_argument("--user", type=str, help= "twitter username", required=True)
    args = parser.parse_args()
    return args



if __name__ == "__main__":
    command_line_args = initialize_argparser()
    startDate = datetime.datetime(2019, 1, 1, 0, 0, 0)
    endDate =   datetime.datetime(2019, 2, 1, 0, 0, 0)


    tweets = tweets_handler.get_tweets(command_line_args.user, startDate.strftime("%Y-%m-%d"), endDate.strftime("%Y-%m-%d"))
    if not tweets:
        print("No tweet found")
    for tweet in tweets:
        p = sentiment_analysis.get_polarity(tweet["text"])
        s = sentiment_analysis.get_subjectivity(tweet["text"])
        print(u"Polarity {}, subjectivity {}".format(p, s))
    
