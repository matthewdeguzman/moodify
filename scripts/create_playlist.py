import spotipy
from spotipy.oauth2 import SpotifyOAuth
from client_credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

#Credentials to access the Spotify Music Data
username = 'madmatt10125'
scope = 'playlist-modify-public'

#Credentials to access the Spotify Music Data
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, username=username, scope=scope))

# Get playlist name from user
# add given tracks to playlist
def create_playlist(playlist_id, items):
    spotify.playlist_add_items(playlist_id, items)
    spotify.playlist_change_details(playlist_id, name='Moodify Playlist', 
    description='A playlist created by Moodify')

items = ['https://open.spotify.com/track/0lizgQ7Qw35od7CYaoMBZb?si=148c36f7308047dc', 
    'https://open.spotify.com/track/0bYg9bo50gSsH3LtXe2SQn?si=686a1602beac426e']
playlist_id = 'https://open.spotify.com/playlist/6MI7UOXyLQCETOCakEGe3B?si=fd565353ffa04bd1'

create_playlist(playlist_id, items)