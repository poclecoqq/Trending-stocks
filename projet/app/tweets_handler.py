import subprocess 
import datetime
import os

def exec_python2(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate() 
    return  output, error


def is_valid_date(_date):
    return isinstance(_date, datetime.date)


def get_path_to_executable():
    cur_abs_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(cur_abs_path, "GetOldTweets-python", "Exporter.py")


def get_tweets(username, start_date, end_date):
    path_to_executable = get_path_to_executable()
    command = "python2 " + path_to_executable + " --username \"" + username + "\" --since " + start_date + " --until " + end_date
    exec_python2(command)