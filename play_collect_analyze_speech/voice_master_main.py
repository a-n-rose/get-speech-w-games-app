#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 15 22:22:15 2018

@author: airos
"""

from voice_master import Mimic_Game
    

if __name__ == '__main__':
    
    currgame = Mimic_Game()
    username = currgame.start_game('start', username = True)
    if username:
        sec = 2
        mictest = currgame.test_mic(sec)
        if mictest == False:
            print("We couldn't test your voice..")
        while currgame.cont_game == True:
            currgame.cont_game = currgame.start_game('listen to a sound')
            if currgame.cont_game:
                currgame.rand_sound2mimic()
            else:
                print("Thanks for playing!")
                currgame.close_game()
            
        
        
         