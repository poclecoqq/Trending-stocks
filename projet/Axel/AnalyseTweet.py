# source : https://www.actuia.com/tutoriel/initiation-a-lanalyse-de-texte-twitter-python-textblob-tweepy/

#TESTER AVEC : 
# ligne de commande pour lancer : python AnalyseTweet.py  --user FinanceCanada 


#import modules

import argparse
import tweepy
from textblob import TextBlob

# Valeure de l'Api twitter
consumer_key = "zr67B9ROvy2PS26gzIXegiwgd"
consumer_secret_key = "onLPhPHRfFc2KX1VF6uzK4J2Mck2pi9hAfY1vAEwbbIKn3eI8C"
access_token = "1241052303907487744-6klxGs4QkGwUUFFxmmTNpntHDR1z5F"
access_token_secret =  "TiQKAWe9wEhiPJp1pXMbXp8CDB8JZYfNBjAhEkHar9afh"


#Mise en place de ce que l'on veut etudier

parser = argparse.ArgumentParser(prog="tweet-analysis", description="Analyse tweet")
parser.add_argument("--user", type=str, help= "twitter username", required=True)
args = parser.parse_args()

# On s'identifie sur tweeter

auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
auth.set_access_token(access_token, access_token_secret)

# On utilise l'api
api = tweepy.API(auth)


#polarite c'est savoir si le tweet est positifou negatif entre -1 et 1
# Subjectivite evalue la subjectivite d'un text entre  0 et 1


nomUtilisateur =  args.user # nom de l'utilisateur que l'on veut
nombreTweet = 200 #nombre de tweet que l'on veut recuperer
# Recupere tout les status d'un tulisateur
for status in api.user_timeline(screen_name = nomUtilisateur, count = nombreTweet):
    print(status.text)
    tweet = TextBlob(status.text)
    print(u"Polarity {}, subjectivity {}".format(tweet.sentiment.polarity, tweet.sentiment.subjectivity))
