from dotenv import load_dotenv
import os
import pandas as pd
from pdb import set_trace as st

def get_spotify_token():
    '''
    This function will initiate the spotify token
    return: spotipy object
    '''

    import spotipy
    import spotipy.util as util
    import sys

    load_dotenv("../.env")
    SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
    SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
    SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
    USERNAME = os.getenv("USERNAME")

    token = util.prompt_for_user_token(
        username=USERNAME,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI
    )

    sp = spotipy.Spotify(auth=token)
    return sp


def load_model():
    import pickle
    import sklearn

    dbfile = open('models/kmeans.pickl', 'rb')
    model = pickle.load(dbfile)
    dbfile.close()
    return model


def load_labled_spotify_songs():
    return pd.read_csv("data/labled_songs_id.csv")


def get_songs_audio_features(song_id_list, spotipy_obj):
    temp_data = spotipy_obj.audio_features(song_id_list)
    spotify_audio_features = pd.DataFrame(temp_data)

    important_features = [
        # "genre",  # spotify genre doesn't match with kaggle genre
        # "popularity",  # don't know how to get it for the song, and it changes over time
        # "key",  # This is categorical
        # "mode",  # this is categorical
        # "time_signature"  # not for now
        "acousticness",
        "danceability",
        "energy",
        "instrumentalness",
        "liveness",
        "loudness",
        "speechiness",
        "tempo",
        "valence",
    ]
    return spotify_audio_features[important_features]


def get_n_similar_songs(song_label, labled_songs, n, spotipy_obj):
    '''
    args:
        song_label: the average song audio features
        labled_songs: the dataframe that has all the
            songs' cluster lables
        n: number of required recommendations
    
    return:
        list of recommended song ids
    '''

    same_cluster_songs = \
        labled_songs[labled_songs["label"] == song_label]\
        .loc[:, "track_id"]
        
    list_of_recommended_songs = same_cluster_songs.head(n).to_list()
    return list_of_recommended_songs
