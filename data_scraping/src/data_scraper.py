import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pathlib import Path
from queue import Queue
import csv
import os

# retrieve parent directory
data_scraping = Path(__file__).resolve().parent.parent

# Retrieve credentials (https://developer.spotify.com/documentation/general/guides/authorization/scopes/)
scope = 'playlist-read-collaborative'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
playlist_data = sp.current_user_playlists()

### Global Variables ###
added_tracks = set()   # list of track_ids added to playlists
added_artists = set() # list of artist_ids added to playlists
data = []   # list of dictionaries containing track data
total_added = 0 # total added tracks

def add_track_data(artist_name, artist_id, album_title, album_id, track_title, track_id):
    '''
    Adds a track to the data.csv file in the specified format
    '''
    global added_tracks
    data.append([{'artist_name': artist_name, 'artist_id': artist_id, 'album_title': album_title, 'album_id': album_id, 'track_title': track_title, 'track_id': track_id}])
    added_tracks.add(track_id)
    
def add_discography(artist_id):
    '''
    Adds all tracks from an artist's albums to the data.csv file
    '''
    # get artist discography and name
    artist_albums = sp.artist_albums(artist_id, album_type='album')['items']
    artist_singles = sp.artist_albums(artist_id, album_type='single')['items']
    artist_name = sp.artist(artist_id)['name']
    global added_artists
    global total_added


    ### adds all albums from user ###
    for album in artist_albums:
        # retrieves album data
        album_id = album['id']
        album_title = album['name']
        album_tracks = sp.album_tracks(album_id)['items']

        # adds each track from the album
        for track in album_tracks:

            # retrieves track data
            track_id = track['id']
            track_title = track['name']

            # write track to data.csv
            add_track_data(artist_name, artist_id, album_title, album_id, track_title, track_id)
            global total_added
            total_added += 1
            if total_added % 1000 == 0:
                print(f'Added {total_added} songs')
    
    ### adds all singles from user ###
    for single in artist_singles:

        # retrieves single data
        single_id = single['id']
        single_title = single['name']
        single_tracks = sp.album_tracks(single_id)['items']

        # adds each track from the single
        for track in single_tracks:

            # retrieves track data
            track_id = track['id']
            track_title = track['name']

            # if the track was already added, continue
            if track_id in added_tracks:
                continue

            # add track to the data
            add_track_data(artist_name, artist_id, single_title, single_id, track_title, track_id)

            total_added += 1
            if total_added % 1000 == 0:
                print(f'Added {total_added} songs')

    # adds the artist to added_artists
    added_artists.add(artist_id)
     
def dfs_add_related_artists(writer, artist_id, iterations, depth):
    '''
    does a depth-first search on the related artists. Only adds a explore iterations
    amount of neighbors and goes up to depth 
    '''

    # if we have already added this artist or we have reached the maximum depth, return
    if artist_id in added_artists or depth <= 0:
        return

    # add the artists' discography
    add_discography(artist_id)

    # get related artists
    related_artists = sp.artist_related_artists(artist_id)['artists']

    # iterate through related artists and call add_related_artists
    for i, artist in enumerate(related_artists):
        if i == iterations:
            break
        dfs_add_related_artists(writer, artist['id'], iterations, depth-1)

def bfs_add_related_artists(initial_artists, iterations):
    '''
    does a breadth-first search on the related artists and adds them. adds up to iterations
    '''
    global total_added

    # initialize the queue by adding all artists in added_artists
    q = Queue()
    for artist in initial_artists:
        q.put(artist)

    while not q.empty():

        # get the next artist and write their data
        artist_id = q.get()
        add_discography(artist_id)

        # if we have reached or surpassed the number of iterations, we return
        if total_added >= iterations:
            return

        # get neighbors
        related_artists = sp.artist_related_artists(artist_id)['artists']
        neighbors = [artist['id'] for artist in related_artists]

        # add neighbors to queue
        for neighbor in neighbors:
            if neighbor not in added_artists:
                q.put(neighbor)

def add_user_playlists():
    '''
    Adds all tracks from a user's playlists to the data
    '''

    # creates a set to stor eall of the artists
    initial_artists = {}

    # iterates through all of the user's playlists
    for playlists in playlist_data['items']:

        # Retrieve number of tracks, loop until all tracks have been added
        num_tracks = playlists['tracks']['total']
        offset = 0

        # Retrieve tracks from playlist
        while offset < num_tracks:
            items = sp.playlist_items(playlists['id'], offset=offset)['items']

            # itereates through each track and adds the artist
            for item in items:
                track = item['track']

                # if the artist has not been added to the list, add it
                if track['artists'][0]['id'] not in initial_artists:
                    initial_artists.add(track['artists'][0]['id'])

            # updates offset
            offset += 100

    # adds related artists using a breadth-first search
    bfs_add_related_artists(initial_artists, 100000) 

def get_track_features(track_ids):
    '''
    Gets the audio features for a list of 100 songs 3 requests per call
    '''

    # Get the data and features of the songs
    meta_data = sp.tracks(track_ids[:50]) + sp.tracks(track_ids[50:])
    features = sp.audio_features(track_ids)

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

def main():
    '''
    Main function which reads and writes all data to data.csv
    '''
    ### Reads Data from data.csv ###
    with open(os.path.join(data_scraping, 'data.csv'), 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            # if we are reading the header, continue
            if line[0] == 'artist_name':
                continue
            
            # Retrieves track_data from csv and adds to data
            track_data = {'artist_name' : line[0], 'artist_id' : line[1], 'album_title' : line[2], 'album_id' : line[3], 'track_title' : line[4], 'track_id' : line[5]}
            data.append(track_data)
            if line[1] not in added_artists:
                added_artists.add(line[1])
            

    ### Collects track data from Spotify and writer to data.csv ###
    # Data will be formatted as follows: artist_name, artist_id, album_track, album_id, track_title, track_id
    with open(os.path.join(data_scraping, 'data.csv'), 'w', encoding='UTF8', newline='') as f:

        # initializes writer and writes header
        writer = csv.writer(f)
        writer.writerow(['artist_name', 'artist_id', 'album_title', 'album_id', 'track_title', 'track_id'])

        ### 1. Add artists from user playlists ###
        add_user_playlists()

        ### 2. Add artists from spotify's playlists ###
        
        ### 3. Write all data to file ###
        for track in data:
            writer.writerow([track['artist_name'], track['artist_id'], track['album_title'], track['album_id'], track['track_title'], track['track_id']])

if __name__ == '__main__':
    main()