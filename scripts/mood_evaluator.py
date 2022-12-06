import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pathlib import Path
import csv
import os

# retrieve parent directory
directory = Path(__file__).resolve().parent.parent

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

    return track_data[:1] + mood_data

def main():
    '''
    Main function which reads and writes all data to track_feaures.csv
    '''
    # Goes through the csv file and reads in the track ids and audio features of the song.
    # The mood of each song is evaluated as well and given an overall mood.
    data = []
    with open(os.path.join(directory, 'track_features.csv'), 'r', encoding='utf-8') as f:

        # reads out the header then intializes the reading object
        next(f)
        reader = csv.reader(f)

        # reads every line in the file and evaluates the
        # mood of the song from the data then appends the data to the data list
        for row in reader:
            data.append(mood_evaluator(row))

    # writes the data to the csv file
    with open(os.path.join(directory, 'track_features.csv'), 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['track_id', 'happy', 'sad', 'calm', 'energy', 'mood'])
        writer.writerows(data)

if __name__ == "__main__":
    main()
    