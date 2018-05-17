#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 15 22:22:15 2018

@author: airos
"""

from voice_master import Mimic_Game
    

if __name__ == '__main__':
    
    new_game = Mimic_Game()
    username = new_game.start_game()
    if username:
        sec = 2
        mictest = new_game.test_mic(sec)
        if mictest == False:
            print("We couldn't test your voice..")