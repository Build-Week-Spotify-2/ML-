import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

# Get the username from terminal
username = sys.argv[1]
# scope = 'user-read-private user-read-playback-state user-modify-playback-state'

# Erase cache and prompt for user permission
try:
    token = util.prompt_for_user_token(username)  # add scope
except (AttributeError, JSONDecodeError):
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username)  # add scope
