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

artist_id = '1z4g3DjTBBZKhvAroFlhOM'    # artists id for 'Red Velvet'
track_ids = ['https://open.spotify.com/track/6dQqQReOLNUG46h9n6l9p1?si=ceeed18f5a51463a', '1FJPXCXDD9yt9naw8R5bfs', '5QpIWR4XQChU7SxdXCoQ4J', '3Qm86XLflmIXVm1wcwkgDK']    # track

meta = spotify.audio_features(['1FJPXCXDD9yt9naw8R5bfs', '5QpIWR4XQChU7SxdXCoQ4J', '3Qm86XLflmIXVm1wcwkgDK'])
print(meta, '\n')
for item in meta:
    print(item, '\n')
# for track_data in meta['tracks']:
#     print(track_data, '\n')
# # receives a list of related artists
# results = spotify.artist_related_artists(artist_id)

# # prints the name of each related artist
# print(results['artists'])
# for element in results['artists']:
#     print(element['name'])
