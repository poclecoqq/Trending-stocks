import subprocess 
import datetime
import os
import csv


def exec_python2(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate() 
    return  output, error


def is_valid_date(_date):
    return isinstance(_date, datetime.date)


def get_path_to_executable():
    cur_abs_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(cur_abs_path, "GetOldTweets-python", "Exporter.py")


def build_command(got_output_file, username=None, start_date=None, end_date=None, query_search=None, maxtweets=None):
    path_to_executable = get_path_to_executable()
    command = "python2 " + path_to_executable + " --output " + got_output_file 
    if maxtweets:
        command = command + " --maxtweets " + str(maxtweets)
    if username:
        command = command + " --username \"" + username + "\""
    if start_date:
        command = command + " --since " + start_date
    if end_date:
        command = command + " --until " + end_date
    if query_search:
        command = command + " --querysearch \"" + query_search + "\""
    return command


def get_tweets(username=None, start_date=None, end_date=None, query_search=None, maxtweets=None,  got_output_file="output_got.csv"):
    command = build_command(got_output_file, username, start_date, end_date, query_search, maxtweets)
    print(command)
    exec_python2(command)
    # GOT (repository) downloads results in a csv file
    t = get_tweets_from_csv(got_output_file)
    delete_file(got_output_file)
    return t

def get_tweets_from_csv(file_name):
    tweets = []
    with open(file_name, 'r') as file:
        reader = csv.reader(file, delimiter = ';')
        next(reader)
        for row in reader:
            try:
                tweet = {"username":row[0], "date":row[1], "retweets":row[2], "favorites":row[3], "text":row[4], "geo":row[5], "mentions":row[6], "hashtags":row[7], "id":row[8], "permalink":row[9]}
                tweets.append(tweet)
            except:
                continue
    return tweets

def delete_file(path):
    if os.path.exists(path):
        os.remove(path)
