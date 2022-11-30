import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Get your credentials from Spotify for Developers
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
artist_id = '1z4g3DjTBBZKhvAroFlhOM'    # artists id for 'Taylor Swift'

# receives a list of related artists
results = spotify.artist_related_artists(artist_id)

# prints the name of each related artist
for element in results['artists']:
    print(element['name'])
