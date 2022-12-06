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

def mood_evaluator(track_data, track_features):
    '''
    Receives a dictionary of track data that contains track features, and each is evaluated with the following
    formulas to evaluate the mood of the song. Each mood is in the range of 0-1 where 0 is the least happy/sad/calm/energetic
    and 1 is the most happy/sad/calm/energetic.

    Happy = 0.15 * danceability + 0.85 * valence
    Sad = 0.85 * (1 - valence) + 0.15 * (0.3energy^2-0.6*energy + 0.3)
    Calm = 0.75 * (1 - energy) + 0.5 / (1 + (loudness + 60)/60)
    Energy = 0.85 * energy + 0.15 * (loudness + 60)/60
    '''

    track_data['happy'] = 0.15 * track_features['danceability'] + 0.85 * track_features['valence']
    track_data['sad'] = 0.85 * (1 - track_features['valence']) + 0.15 * (0.3 * track_features['energy'] ** 2 - 0.6 * track_features['energy'] + 0.3)
    track_data['calm'] = 0.75 * (1-track_features['energy']) + 0.5 / (1 + (track_features['loudness'] + 60) / 60) - 0.25
    track_data['energy'] = 0.85 * track_features['energy'] + 0.15 * (track_features['loudness'] + 60) / 60 

print(spotify.track('2vuDdXqekkDCSdawJyUpT6'))
# for track_data in meta['tracks']:
#     print(track_data, '\n')
# # receives a list of related artists
# results = spotify.artist_related_artists(artist_id)

# # prints the name of each related artist
# print(results['artists'])
# for element in results['artists']:
#     print(element['name'])

