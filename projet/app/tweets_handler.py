import tweepy
from threading import Lock
import math

consumer_key = "zr67B9ROvy2PS26gzIXegiwgd"
consumer_secret_key = "onLPhPHRfFc2KX1VF6uzK4J2Mck2pi9hAfY1vAEwbbIKn3eI8C"
access_token = "1241052303907487744-6klxGs4QkGwUUFFxmmTNpntHDR1z5F"
access_token_secret =  "TiQKAWe9wEhiPJp1pXMbXp8CDB8JZYfNBjAhEkHar9afh"

lock = Lock()
api = None

# constants
MAX_TWEETS = 3200 #Twitter ne conserve que les 3200 tweets les plus récents
REQUEST_SIZE = 200

def authentify(key=consumer_key, secret_key=consumer_secret_key, token=access_token, secret_token=access_token_secret):
    global api
    auth = tweepy.OAuthHandler(key, secret_key)
    auth.set_access_token(token, secret_token)
    lock.acquire()
    api = tweepy.API(auth)
    lock.release() 


def get_tweets_by_user(username, nb = REQUEST_SIZE):
    return api.user_timeline(screen_name = username, count = nb)

def get_tweets_before_tweetid(username, before_id, nb = REQUEST_SIZE):
    return api.user_timeline(screen_name = username, count = nb, max_id = before_id)

def in_period_tweets(tweets, start_date, end_date):
    r_tweets = []
    for tweet in tweets:
        if tweet.created_at < end_date and tweet.created_at > start_date:
            r_tweets.append(tweet)
    return r_tweets

def are_tweets_too_old(tweets, start_date):
    return tweets[0].created_at < start_date
     

def get_tweets_in_period(username, start_date, end_date):
    tweets = []
    max_request_nb = math.ceil(MAX_TWEETS/REQUEST_SIZE)

    tmpTweets = get_tweets_by_user(username)
    for _ in range(0, max_request_nb):
        print(tmpTweets[0].created_at)
        if are_tweets_too_old(tmpTweets, start_date):
            break
        tweets.extend(in_period_tweets(tmpTweets, start_date, end_date))
        tmpTweets = get_tweets_before_tweetid(username, tmpTweets[-1].id)
    return tweets
