track_dict = {}

with open('track_features.txt') as f:
    for line in f:
        values = line.split(',')

        track_id = values[0]
        happy = values[1]
        sad = values[2]
        calm = values[3]
        energy = values[4]
        mood = values[5]

        track_dict[track_id] = {
            'happy': happy,
            'sad': sad,
            'calm': calm,
            'energy': energy,
            'mood': mood
        }
    
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

    print("Welcome to Moodify! We're going to help you find the perfect song for your mood.")
    print("How long would you like the playlist to be? (1-50)")
    playlist_length = int(input())
    print("What is your Spotify username?")
    username = input()
    print("Link to playlist:")
    print("https://open.spotify.com/user/" + username + "/playlist/") #????
    print("What sorting algorithm would you like to use? (1 for quicksort, 2 for mergesort)")
    sort = input()
    print()

    print("Questionnaire to determine your mood:")
    print("1. How good are you feeling today? (Scale of 1-5)(1 is awful, 5 is great)")
    feeling = input("Answer: ")
    print("2. How good do you expect the rest of the day to be? (Scale of 1-5)(1 is awful, 5 is amazing)")
    expect = input("Answer: ")
    print("3. Do you want to be left alone? (Scale of 1-5)(1 is strongly agree, 5 is a strongly disagree)")
    alone = input("Answer: ")
    print("4. Do you feel overwhelmed by work or studies? (Scale of 1-5)(1 is strongly agree, 5 is a strongly disagree)")
    work = input("Answer: ")
    print("5 What activity most closely describes your activity whilst listening to music? (1 is Exercising, 2 is Working, 3 is Relaxing)")
    activity = input("Answer: ")
    
    
