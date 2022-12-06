'''
Given the answers to the user's survey regarding their feelings and activity,
this script evaluates their mood.

min sadness = (sad: 0.1, calm: 0., happy: )
1. How good are you feeling today (Scale of 1-5) (1|2)-> sad, 3->calm, 4 happy, 5 happy and energetic
if 1: sad += 0.2 and calm += 0.1 and happy += 0.05 and energy += 0.05
if 2: sad += 0.15 and calm += 0.15 and happy = 0.1 and energy += 0.075
if 3: sad += 0.05 and calm += 0.2 and happy += 0.15 and energy += 0.1
if 4: sad += 0.01 and calm += 0.1 and happy += 0.2 and energy += 0.15
if 5: sad += 0.005 and calm += 0.1 and happy += 0.25 and energy += 0.2

2. How good do you expect the rest of the day to be (Scale of 1-5) same as above
if 1: sad += 0.35 and calm += 0.1 and happy += 0.05 and energy += 0.05
if 2: sad += 0.3 and calm += 0.125 and happy = 0.1 and energy += 0.075
if 3: sad += 0.1 and calm += 0.15 and happy += 0.15 and energy += 0.1
if 4: sad += 0.05 and calm += 0.1 and happy += 0.2 and energy += 0.15
if 5: sad += 0.01 and calm += 0.1 and happy += 0.25 and energy += 0.2

3. Do you want to be left alone (Scale of 1-5) 1-> sad, 2-> calm, 3-> calm and happy, (4|5) -> happy and 
energetic
if 1: sad += 0.2 and calm += 0.1 and happy += 0.05 and energy += 0.05
if 2: sad += 0.1 and calm += 0.2 and happy += 0.1 and energy += 0.075
if 3: sad += 0.05 and calm += 0.25 and happy += 0.15 and energy += 0.1
if 4: sad += 0.01 and calm += 0.15 and happy += 0.2 and energy += 0.125
if 5: sad += 0.005 and calm += 0.1 and happy += 0.25 and energy += 0.15

4. Do you feel overwhelmed by work or studies (Scale of 1-5) 1-> sad and calm, 2-> sad and calm, 3-> calm, 
(4|5)-> happy and calm
if 1: sad += 0.2 and calm += 0.2 and happy += 0.01 and energy += 0.05
if 2: sad += 0.1 and calm += 0.225 and happy += 0.05 and energy += 0.075
if 3: sad += 0.05 and calm += 0.25 and happy += 0.075 and energy += 0.1
if 4: sad += 0.1 and calm += 0.15 and happy += 0.1 and energy += 0.125
if 5: sad += 0.05 and calm += 0.1 and happy += 0.15 and energy += 0.15

5. What activity most closely describes your activity whilst listening? Exercising -> energetic, working -> 
calm, relaxing -> calm and happy
if Exercising: sad += 0.01 and calm += 0.05 and happy += 0.1 and energy += 0.3
if Working: sad += 0.05 and calm += 0.1 and happy += 0.075 and energy += 0.15
if Relaxing: sad += 0.05 and calm += 0.15 and happy += 0.1 and energy += 0.05
'''
