from pathlib import Path
from random import randint
import os
import csv

directory = Path(__file__).resolve().parent.parent
file_name = 'track_features.csv'

def retrieve_songs(user_emotions, max_songs):
    '''
    Given a user's mood values, the script looks in track_features.csv for songs that match the user's mood.
    For a song to match the user's mood, the songs emotions must be within 15% of the user's emotions. The overall
    closeness of a song will have be the sum of all emotional closeness to the user (E_i-U_i)^2 
    '''
    playlist = []
    added_tracks = set()
    track_data = []

    # Retrieves the data from track_features.csv
    with open(os.path.join(directory, file_name), 'r', encoding='utf-8') as f:
        next(f)
        reader = csv.reader(f)
        for row in reader:
            # Each row is formatted as such [track_id, happy, sad, calm, energy, mood]
            # appends each row to the data
            track_data.append(row)

    # search randomly through tracks until we find the maximum number of songs close to the user's mood
    while(len(playlist) < max_songs):

        # retrieve a random index
        index = randint(0, len(track_data)-1)
        # if we have already added the track, we skip it
        if track_data[index][0] in added_tracks:
            continue

        track_emotions = track_data[index][1:5] # holds the emotions of the song
        within_range = 0 # boolean that determines if the song is within the user's mood
        
        # iterates through the emotions of the song and determines if the song is within the user's mood
        for i in range(len(user_emotions)):
            # if the emotion is not within 15% of the user's emotion, the song is not added to the playlist
            variance = float(track_emotions[i]) / float(user_emotions[i])
            if not (variance < 0.85 or variance > 1.15):
                within_range += 1

        # if the song is within the user's mood, we add it to the playlist
        if within_range >= 2:
            closeness = 0
            for i in range(len(user_emotions)):
                closeness += (float(track_emotions[i]) - float(user_emotions[i])) ** 2

            playlist.append((track_data[index][0], closeness))
            added_tracks.add(track_data[index][0])

    return playlist




