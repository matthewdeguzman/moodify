from pathlib import Path
from random import randint
from client_credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
import os
import csv

directory = Path(__file__).resolve().parent.parent
scope = 'playlist-modify-public'

def ask_question(question, valid_responses=None):
    '''
    Asks a question and returns the user's response
    '''
    valid_response = False
    while not valid_response:
        print(question, end='')
        response = input()
        if valid_responses is None or response in valid_responses:
            return response
        else:
            print("Invalid response. Please try again.")

def evaluate_mood(user_responses):
    '''
    Evaluates the user's mood based off of their survey responses and
    returns a dict with the representations of their mood
    '''
    mood_list = [0.0, 0.0, 0.0, 0.0]    # happy, sad, calm, and energy

    def assign_values(sad, calm, happy, energy):
        mood_list[0] += happy
        mood_list[1] += sad
        mood_list[2] += calm
        mood_list[3] += energy

    if user_responses[0] == 1:
        assign_values(0.2, 0.1, 0.05, 0.05)
    elif user_responses[0] == 2:
        assign_values(0.15, 0.15, 0.1, 0.075)
    elif user_responses[0] == 3:
        assign_values(0.05, 0.2, 0.15, 0.1)
    elif user_responses[0] == 4:
        assign_values(0.01, 0.1, 0.2, 0.15)
    elif user_responses[0] == 5:
        assign_values(0.005, 0.1, 0.25, 0.2)

    if user_responses[1] == 1:
        assign_values(0.35, 0.1, 0.05, 0.05)
    elif user_responses[1] == 2:
        assign_values(0.3, 0.125, 0.1, 0.075)
    elif user_responses[1] == 3:
        assign_values(0.1, 0.15, 0.15, 0.1)
    elif user_responses[1] == 4:
        assign_values(0.05, 0.1, 0.2, 0.15)
    elif user_responses[1] == 5:
        assign_values(0.01, 0.1, 0.25, 0.2)

    if user_responses[2] == 1:
        assign_values(0.2, 0.1, 0.05, 0.05)
    elif user_responses[2] == 2:
        assign_values(0.1, 0.2, 0.1, 0.075)
    elif user_responses[2] == 3:
        assign_values(0.05, 0.25, 0.15, 0.1)
    elif user_responses[2] == 4:
        assign_values(0.01, 0.15, 0.2, 0.125)
    elif user_responses[2] == 5:
        assign_values(0.005, 0.1, 0.25, 0.15)

    if user_responses[3] == 1:
        assign_values(0.2, 0.2, 0.01, 0.05)
    elif user_responses[3] == 2:
        assign_values(0.1, 0.225, 0.05, 0.075)
    elif user_responses[3] == 3:
        assign_values(0.05, 0.25, 0.075, 0.1)
    elif user_responses[3] == 4:
        assign_values(0.1, 0.15, 0.1, 0.125)
    elif user_responses[4] == 5:
        assign_values(0.05, 0.1, 0.15, 0.15)

    if user_responses[4] == 1:
        assign_values(0.01, 0.05, 0.1, 0.3)
    elif user_responses[4] == 2:
        assign_values(0.05, 0.1, 0.075, 0.15)
    elif user_responses[4] == 3:
        assign_values(0.05, 0.15, 0.1, 0.05)

    return mood_list

def print_logo():
    '''
    Prints the moodify logo
    '''
    print("""
    ⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⣶⣶⣶⣶⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⢀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀⠀⠀⠀⠀
    ⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀
    ⠀⢀⣾⣿⡿⠿⠛⠛⠛⠉⠉⠉⠉⠛⠛⠛⠿⠿⣿⣿⣿⣿⣿⣷⡀⠀
    ⠀⣾⣿⣿⣇⠀⣀⣀⣠⣤⣤⣤⣤⣤⣀⣀⠀⠀⠀⠈⠙⠻⣿⣿⣷⠀
    ⢠⣿⣿⣿⣿⡿⠿⠟⠛⠛⠛⠛⠛⠛⠻⠿⢿⣿⣶⣤⣀⣠⣿⣿⣿⡄
    ⢸⣿⣿⣿⣿⣇⣀⣀⣤⣤⣤⣤⣤⣄⣀⣀⠀⠀⠉⠛⢿⣿⣿⣿⣿⡇
    ⠘⣿⣿⣿⣿⣿⠿⠿⠛⠛⠛⠛⠛⠛⠿⠿⣿⣶⣦⣤⣾⣿⣿⣿⣿⠃
    ⠀⢿⣿⣿⣿⣿⣤⣤⣤⣤⣶⣶⣦⣤⣤⣄⡀⠈⠙⣿⣿⣿⣿⣿⡿⠀
    ⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣿⡿⠁⠀
    ⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀⠀
    ⠀⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠁⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⠛⠿⠿⠿⠿⠛⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀""")
    print("""
                                                                        
                                            ,,    ,,      ,...         
    `7MMM.     ,MMF'                        `7MM    db    .d' ""         
    MMMb    dPMM                            MM          dM`            
    M YM   ,M MM  ,pW"Wq.   ,pW"Wq.    ,M""bMM  `7MM   mMMmm`7M'   `MF'
    M  Mb  M' MM 6W'   `Wb 6W'   `Wb ,AP    MM    MM    MM    VA   ,V  
    M  YM.P'  MM 8M     M8 8M     M8 8MI    MM    MM    MM     VA ,V   
    M  `YM'   MM YA.   ,A9 YA.   ,A9 `Mb    MM    MM    MM      VVV    
    .JML. `'  .JMML.`Ybmd9'   `Ybmd9'   `Wbmd"MML..JMML..JMML.    ,V     
                                                                ,V      
                                                            OOb"       
    """)

def conduct_survey():
    emotional_resp = [0, 0, 0, 0, 0]
    user_emotions = {}

    print("Welcome to Moodify! We're going to help you find the perfect song for your mood.")
    playlist_length = int(ask_question('How long would you like the playlist to be? (1-50) ', valid_responses=[str(i) for i in range(1, 51)]))
    # playlist_id = ask_question('What is the link of the playlist you would like to add songs to? ')
    # username = ask_question('What is your Spotify username? ')
    sort_choice = ask_question('What sorting algorithm would you like to use? (1 for quicksort, 2 for mergesort) ' , valid_responses=['1', '2'])
    

    print("Questionnaire to determine your mood:")
    emotional_resp[0] = int(ask_question('1. On a scale of 1 through 5, how good are you feeling today? (1 is awful, 5 is amazing) ', valid_responses=[str(i) for i in range(1, 6)]))
    emotional_resp[1] = int(ask_question('2. On a scale of 1 through 5, how good do you expect the rest of the day to be? (1 is awful, 5 is amazing) ', valid_responses=[str(i) for i in range(1, 6)]))
    emotional_resp[2] = int(ask_question('3. On a scale of 1 through 5, Do you want to be left alone? (1 is strongly agree, 5 is a strongly disagree) ', valid_responses=[str(i) for i in range(1, 6)]))
    emotional_resp[3] = int(ask_question('4. On a scale of 1 through 5, Do you feel overwhelmed by work or studies? (1 is strongly agree, 5 is a strongly disagree) ', valid_responses=[str(i) for i in range(1, 6)]))
    emotional_resp[4] = int(ask_question('5. What activity most closely describes your activity whilst listening to music? (1 is Exercising, 2 is Working, 3 is Relaxing) ', valid_responses=['1', '2', '3']))

    user_emotions = evaluate_mood(emotional_resp)
    return playlist_length, sort_choice, user_emotions

def retrieve_songs(user_emotions, max_songs):
    '''
    Given a user's mood values, the script looks in track_features.csv for songs that match the user's mood.
    For a song to match the user's mood, the songs emotions must be within 15% of the user's emotions. The overall
    closeness of a song will have be the sum of all emotional closeness to the user (E_i-U_i)^2 

    user_emotions will be a list in the format [happy, sad, calm, energy]
    '''

    playlist = []
    added_tracks = set()
    track_data = []

    # Retrieves the data from track_features.csv
    with open(os.path.join(directory, 'track_features.csv'), 'r', encoding='utf-8') as f:
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

def main():
    print_logo()
    playlist_length, sort_choice, user_emotions = conduct_survey()
    playlist = retrieve_songs(user_emotions, playlist_length)
    pl = [playlist[i][0] for i in range(len(playlist))]
    spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=scope))

    spotify.user_playlist_create(user='madmatt10125', name='Moodify Playlist', description='A playlist created by Moodify')
    playlist_id = ''
    offset = 0
    while playlist_id == '':
        playlists = spotify.current_user_playlists(limit=50, offset=offset)
        
        for playlist in playlists['items']:
            if playlist['name'] == 'Moodify Playlist':
                playlist_id = playlist['id']
                break

        offset += 50
    print(playlist_id)
    spotify.user_playlist_add_tracks(user='madmatt10125', playlist_id=playlist_id, tracks=pl)
    



if __name__ == '__main__':
    main()