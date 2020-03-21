import argparse

from app import news_handler, sentiment_analysis, tweets_handler

def initialize_argparser():
    parser = argparse.ArgumentParser(prog="tweet-analysis", description="Analyse tweet")
    parser.add_argument("--user", type=str, help= "twitter username", required=True)
    args = parser.parse_args()
    return args



if __name__ == "__main__":
    command_line_args = initialize_argparser()
    tweets_handler.authentify()
    tweets = tweets_handler.get_tweets_by_user(command_line_args.user, 200)
    for tweet in tweets:
        p = sentiment_analysis.get_polarity(tweet.text)
        s = sentiment_analysis.get_subjectivity(tweet.text)
        print(u"Polarity {}, subjectivity {}".format(p, s))
    
