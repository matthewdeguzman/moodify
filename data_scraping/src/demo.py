import spotipy
from spotipy.oauth2 import SpotifyOAuth
scope = 'playlist-read-collaborative'
# Get your credentials from Spotify for Developers
spotify = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))
artist_id = '1z4g3DjTBBZKhvAroFlhOM'    # artists id for 'Red Velvet'

# # receives a list of related artists
# results = spotify.artist_related_artists(artist_id)

# # prints the name of each related artist
# print(results['artists'])
# for element in results['artists']:
#     print(element['name'])
print('working...')
artist_singles = spotify.artist_albums(artist_id, album_type='album')['items']
print(artist_singles[0])