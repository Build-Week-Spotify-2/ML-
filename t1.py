import spotipy
import spotipy.util as util
import sys

SPOTIPY_CLIENT_ID='87d5ab3264f5406cb565552216721155'
SPOTIPY_CLIENT_SECRET='de9f2fcefcdb4fcea3923fb0fe2a088a'
SPOTIPY_REDIRECT_URI='https://google.com/'
USERNAME = "2d8351ybzd0df9csxzcs7unh6"


from pdb import set_trace as st
# scope = 'user-library-read'

# if len(sys.argv) > 1:
#     username = sys.argv[1]
# else:
#     print("Usage: %s username" % (sys.argv[0],))
#     sys.exit()
# spotify:user:2d8351ybzd0df9csxzcs7unh6
token = util.prompt_for_user_token(
    username=USERNAME,
    # scope,
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI
)
# token = util.prompt_for_user_token(username, scope)
sp = spotipy.Spotify(auth=token)
st()
# strack
# if token:
#     sp = spotipy.Spotify(auth=token)
#     results = sp.current_user_saved_tracks()
#     for item in results['items']:
#         track = item['track']
#         print(track['name'] + ' - ' + track['artists'][0]['name'])
# else:
#     print("Can't get token for", username)




# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials

# birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
# spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

# results = spotify.artist_albums(birdy_uri, album_type='album')
# albums = results['items']
# while results['next']:
#     results = spotify.next(results)
#     albums.extend(results['items'])

# for album in albums:
#     print(album['name'])