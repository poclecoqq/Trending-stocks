import os
import pickle

saved_data_floder = os.path.join(os.path.dirname(os.path.abspath(__file__)),"saved_data") 
if not os.path.exists(saved_data_floder):
    os.makedirs(saved_data_floder)


def save_data(tweets, filename="saved_data"):
    file_path = os.path.join(saved_data_floder,filename)
    with open(file_path, "wb") as file:
        pickle.dump(tweets, file)

def get_saved_data(filename="saved_data"):
    tweets = []
    file_path = os.path.join(saved_data_floder,filename)
    with open(file_path, "rb") as file:
        tweets = pickle.load(file)
    return tweets