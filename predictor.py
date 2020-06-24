from methods import methods
from pdb import set_trace as st
import pandas as pd

def predict(song_id_list, recommendation_count):

    # get spotipy token
    spotipy_obj = methods.get_spotify_token()

    # load ML model
    kmeans_model = methods.load_model()

    # load labled KMeans data
    labled_songs_df = methods.load_labled_spotify_songs()  # ["song_id"] -> lable. returns dataframe

    input_songs_audio_features = methods.get_songs_audio_features(song_id_list, spotipy_obj)   
    average_song_features = input_songs_audio_features.mean()
    average_song_cluster_label = kmeans_model.predict([average_song_features])
    similar_song_id_list = methods.get_n_similar_songs(
        average_song_cluster_label[0],
        labled_songs_df,
        recommendation_count,
        spotipy_obj
    )

    # st()
    output_df = methods.get_songs_audio_features(similar_song_id_list, spotipy_obj)   
    output_df["song_id"] = similar_song_id_list
    # output_df = 

    return output_df


if __name__ == "__main__":
    song_id_list = [
        "7FGq80cy8juXBCD2nrqdWU",
        "20hsdn8oITBsuWNLhzr5eh",
        "7fPuWrlpwDcHm5aHCH5D9t",
        "67O8CWXxPsfz8orZVGMQwf",
        "2BOqDYLOJBiMOXShCV1neZ",
    ]

    print(predict(song_id_list, 5))
