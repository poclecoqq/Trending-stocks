from textblob import TextBlob


def tweets_to_sentiment(tweets):
    stocks_polarity = {}
    if not tweets:
        exit("No tweet found")
    else:
        for tweet in tweets:
            p = TextBlob(tweet["text"]).sentiment.polarity
            if p:
                s = TextBlob(tweet["text"]).sentiment.subjectivity
                if not tweet["stock"] in stocks_polarity:
                    stocks_polarity[tweet["stock"]] = [(p,s)]
                else:
                    stocks_polarity[tweet["stock"]].append((p,s))
    if not stocks_polarity:
        exit("Could not extract polarity from given tweets. Program finished.")
    return stocks_polarity

def stocks_average_sentiment(tweets_sentiment):
    result = {}
    for stock in tweets_sentiment.keys():
        tot_polarity = 0
        tot_subjectivity = 0
        elem_nb = len(tweets_sentiment[stock])
        for sa in tweets_sentiment[stock]:
            tot_polarity += sa[0]
            tot_subjectivity += sa[1]
        result[stock] = (tot_polarity/elem_nb, tot_subjectivity/elem_nb)
    return result

def get_stock_sentiment(tweets):
    tweets_sentiment = tweets_to_sentiment(tweets)
    stock_sentiment = stocks_average_sentiment(tweets_sentiment)
    return stock_sentiment
