#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 15 22:22:15 2018

@author: airos
"""

from voice_master import Mimic_Game

if __name__ == '__main__':
    print("Welcome to the Mimic Mastery Game!")
    user_ready = input("Press ENTER to start")
    user_start = False
    while user_start == False:
        if user_ready:
            user_ready = input("Press ENTER to start. To exit, type 'exit': ")
            if 'exit' in user_ready.lower():
                break
        else:
            user_start = True
    
    username = input("What's your name? ")
    user_game = Mimic_Game(username)
    
    test_start = input("Ready to test your mic? (press y or n): ")
    test = False
    while test == False:
        if 'n' in test_start:
            print("Why did you start the game then? Give it a try!")
        if 'y' in test_start:
            test = True
    print("Recoring...")
    user_rec = user_game.test_record()
    print("Stopped recording and.....")
    if user_rec.any():
        print("It worked!")
        print("And here's how you sounded:")
        user_game.play_rec(user_rec)
    else:
        print("Oh darnit... Something's wrong...")
        
    
        