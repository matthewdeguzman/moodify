import spotipy
from spotipy.oauth2 import SpotifyOAuth
scope = 'playlist-read-collaborative'

# Get your credentials from Spotify for Developers
client_id='902386052a87438185e83043720ed2b2'
client_secret='a9997a3d84994fd7b7f1c09d3419a0b1'
redirect_uri='https://localhost:8888/callback'
username = 'madmatt10125'
scope = 'playlist-modify-public'

#Credentials to access the Spotify Music Data
manager = spotipy.SpotifyClientCredentials(client_id,client_secret)
spotify = spotipy.Spotify(client_credentials_manager=manager)

print(spotify.user('madmatt10125'))

