#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 15 22:22:15 2018

@author: airos
"""

from voice_master import Mimic_Game


def start_game():
    user_ready = input("Press ENTER to start or type 'exit' to leave: ")
    if user_ready == '':
        user_name = input("Great! What will be your username?: ")
        return user_name
    elif 'exit' in user_ready.lower():
        return None
    else:
        start_game()
    
    

if __name__ == '__main__':
    print("Welcome to the Mimic Mastery Game!")
    username = start_game()
    if username:
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
            
        
            