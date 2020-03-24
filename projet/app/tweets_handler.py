import tweepy
from threading import Lock

consumer_key = "zr67B9ROvy2PS26gzIXegiwgd"
consumer_secret_key = "onLPhPHRfFc2KX1VF6uzK4J2Mck2pi9hAfY1vAEwbbIKn3eI8C"
access_token = "1241052303907487744-6klxGs4QkGwUUFFxmmTNpntHDR1z5F"
access_token_secret =  "TiQKAWe9wEhiPJp1pXMbXp8CDB8JZYfNBjAhEkHar9afh"

lock = Lock()
api = None


def authentify(key=consumer_key, secret_key=consumer_secret_key, token=access_token, secret_token=access_token_secret):
    global api
    auth = tweepy.OAuthHandler(key, secret_key)
    auth.set_access_token(token, secret_token)
    lock.acquire()
    api = tweepy.API(auth)
    lock.release() 


def get_tweets_by_user(user, nb):
    return api.user_timeline(screen_name = user, count = nb)
