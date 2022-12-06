import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pathlib import Path
import csv
import os

# retrieve parent directory
directory = Path(__file__).resolve().parent.parent.parent

# Retrieve credentials (https://developer.spotify.com/documentation/general/guides/authorization/scopes/)
# Get your credentials from Spotify for Developers
client_id='902386052a87438185e83043720ed2b2'
client_secret='a9997a3d84994fd7b7f1c09d3419a0b1'
redirect_uri='https://localhost:8888/callback'
username = 'madmatt10125'
scope = 'playlist-modify-public'

#Credentials to access the Spotify Music Data
manager = spotipy.SpotifyClientCredentials(client_id,client_secret)
spotify = spotipy.Spotify(client_credentials_manager=manager)

### Global Variables ###
data = []   # list of dictionaries containing track data

def add_track_data(artist_name, artist_id, album_title, album_id, track_title, track_id, mood):
    '''
    Adds a track to the data.csv file in the specified format
    '''
    global added_tracks
    data.append([{'artist_name': artist_name, 'artist_id': artist_id, 'album_title': album_title, 'album_id': album_id, 
    'track_title': track_title, 'track_id': track_id, 'happy': mood['happy'], 'sad': mood['sad'], 'calm': mood['calm'], 
    'energy': mood['energy']}])
    

def get_track_features(track_ids):
    '''
    Gets the audio features for a list of 100 songs 3 requests per call
    '''

    # Get the data and features of the songs
    meta_data = spotify.tracks(track_ids[:50]) + sp.tracks(track_ids[50:])
    features = spotify.audio_features(track_ids)

    # map that will hold the data for each each song
    data = {track_ids[i] : {} for i in range(track_ids)}
    # meta
    
    # puts track data in data
    for track_data in meta_data['tracks']:
        data[track_data['id']]['name'] = track_data['name']
        data[track_data['id']]['album'] = track_data['album']['name']
        data[track_data['id']]['artist'] = track_data['album']['artists'][0]['name']
        data[track_data['id']]['release_date'] = track_data['album']['release_date']
        data[track_data['id']]['length'] = track_data['duration_ms']
        data[track_data['id']]['popularity'] = track_data['popularity']

    # inserts the track_features into the map
    for track_feature in features:
        track_id = track_feature['id']
        data[track_id]['features'] = {}
        data[track_id]['features']['acousticness'] = track_feature['acousticness']
        data[track_id]['features']['danceability'] = track_feature['danceability']
        data[track_id]['features']['energy'] = track_feature['energy']
        data[track_id]['features']['instrumentalness'] = track_feature['instrumentalness']
        data[track_id]['features']['liveness'] = track_feature['liveness']
        data[track_id]['features']['loudness'] = track_feature['loudness']
        data[track_id]['features']['valence'] = track_feature['valence']
        data[track_id]['features']['speechiness'] = track_feature['speechiness']
        data[track_id]['features']['tempo'] = track_feature['tempo']
        data[track_id]['features']['key'] = track_feature['key']
        data[track_id]['features']['time_signature'] = track_feature['time_signature']

    return data

def mood_evaluator(track_data):
    '''
    Receives a dictionary of track data that contains track features, and each is evaluated with the following
    formulas to evaluate the mood of the song. Each mood is in the range of 0-1 where 0 is the least happy/sad/calm/energetic
    and 1 is the most happy/sad/calm/energetic.

    Happy = 0.15 * danceability + 0.85 * valence
    Sad = 0.85 * (1 - valence) + 0.15 * (0.3energy^2-0.6*energy + 0.3)
    Calm = 0.75 * (1 - energy) + 0.5 / (1 + (loudness + 60)/60)
    Energy = 0.85 * energy + 0.15 * (loudness + 60)/60
    '''
    # gets track features and calculates the emotions from them
    danceability = float(track_data[1])
    energy = float(track_data[2])
    loudness = float(track_data[3])
    valence = float(track_data[4])

    happy = 0.15 * danceability + 0.85 * valence
    sad = 0.85 * (1 - valence) + 0.15 * (0.3 * energy ** 2 - 0.6 * energy + 0.3)
    calm = 0.75 * (1-energy) + 0.5 / (1 + (loudness + 60) / 60) - 0.25
    energy = 0.85 * energy + 0.15 * (loudness + 60) / 60 

    # records the emotions in a list and appens the emotion with the highest value to the list
    mood_data = [happy, sad, calm, energy]
    most_mood = max(mood_data)

    if most_mood == happy:
        mood_data.append("happy")
    elif most_mood == sad:
        mood_data.append("sad")
    elif most_mood == calm:
        mood_data.append("calm")
    else:
        mood_data.append("energetic")
    
    track_data += mood_data

def main():
    '''
    Main function which reads and writes all data to data.csv
    '''
    # Goes through the csv file and reads in the track ids and audio features of the song.
    # The mood of each song is evaluated as well and given an overall mood.
    data = []
    with open(os.path.join(directory, 'track_features.csv'), 'r', encoding='utf-8') as f:

        # reads out the header then intializes the reading object
        next(f)
        reader = csv.reader(f)

        # reads every line in the file and evaluates the
        #  mood of the song from the data then appends the data to the data list
        for row in reader:
            mood_evaluator(row)
            data.append(row)

    # writes the data to the csv file
    with open(os.path.join(directory, 'track_features.csv'), 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['track_id', 'danceability', 'energy', 'loudness', 'valence', 'happy', 'sad', 'calm', 'energy', 'mood'])
        writer.writerows(data)
    
if __name__ == '__main__':
    main()