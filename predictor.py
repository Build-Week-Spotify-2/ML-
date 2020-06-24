import pandas as pd
import os
from dotenv import load_dotenv
from pdb import set_trace as st


def predict(song_id_list, recommendation_count):
    
    def get_spotify_token():
        '''
        This function will initiate the spotify token
        return: spotipy object
        '''

        import spotipy
        import spotipy.util as util
        import sys

        load_dotenv()
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

        dbfile = open('./kmeans.pickl', 'rb')
        model = pickle.load(dbfile)
        dbfile.close()
        return model

    def load_labled_spotify_songs():
        return pd.read_csv("./labled_songs_id.csv")

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

    def main(song_id_list, recommendation_count):
        # get spotipy token
        spotipy_obj = get_spotify_token()

        # load ML model
        kmeans_model = load_model()

        # load labled KMeans data
        labled_songs_df = load_labled_spotify_songs()  # ["song_id"] -> lable. returns dataframe

        input_songs_audio_features = get_songs_audio_features(song_id_list, spotipy_obj)   
        average_song_features = input_songs_audio_features.mean()
        average_song_cluster_label = kmeans_model.predict([average_song_features])
        similar_song_id_list = get_n_similar_songs(
            average_song_cluster_label[0],
            labled_songs_df,
            recommendation_count,
            spotipy_obj
        )

        output_df = get_songs_audio_features(similar_song_id_list, spotipy_obj)

        return output_df

    return main(song_id_list, recommendation_count)


if __name__ == "__main__":
    song_id_list = [
        "7FGq80cy8juXBCD2nrqdWU",
        "20hsdn8oITBsuWNLhzr5eh",
        "7fPuWrlpwDcHm5aHCH5D9t",
        "67O8CWXxPsfz8orZVGMQwf",
        "2BOqDYLOJBiMOXShCV1neZ",
    ]

    print(predict(song_id_list, 5))
