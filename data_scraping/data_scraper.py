import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Retrieve credentials
scope = "playlist-read-collaborative"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

results = sp.current_user_playlists()

for playlists in results['items']:
    print(playlists, '\n')