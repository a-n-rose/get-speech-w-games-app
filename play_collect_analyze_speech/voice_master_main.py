#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 15 22:22:15 2018

@author: airos
"""

from voice_master import Mimic_Game
import datetime
import os
    

if __name__ == '__main__':
    currgame = Mimic_Game()
    username = currgame.start_game('start', username = True)
    max_points = 1000
    directory_mim = './soundfiles/'
    directory_user = './user_recordings/'
    if not os.path.exists(directory_user):
        os.makedirs(directory_user)
    if username:
        sec = 5
        test_mic = currgame.start_game('test your mic')
        if test_mic:
            print("Now recording")
        mictest = currgame.test_mic(sec)
        if mictest == False:
            print("We couldn't test your voice..")
        while currgame.cont_game == True:
            while currgame.points < max_points:
                currgame.cont_game = currgame.start_game('listen to a sound')
                if currgame.cont_game:
                    print("Right after this plays, we will record your attempt at the sound. Get ready!")
                    mim_filename = directory_mim+currgame.rand_sound2mimic()
                    duration = currgame.get_duration(mim_filename)
                    max_amp = currgame.get_max_amp(mim_filename)
                    rep_mim = currgame.record_user(duration)
                    
                    #save the recording
                    time = datetime.datetime.now()
                    time_str = currgame.get_date()
                    usr_recfilename = directory_user+username+'_'+time_str+'.wav'
                    currgame.save_rec(usr_recfilename,rep_mim,fs=44100)
                    
                    currgame.match_amp(usr_recfilename,max_amp)
                    
                    currgame.play_wav(usr_recfilename)
                    print("\nNot bad, {}!\n".format(currgame.username))
                    
                    fingpr_mim = currgame.get_fingpr(mim_filename)
                    fingpr_usr = currgame.get_fingpr(usr_recfilename)
                    score = currgame.comp_fingpr(fingpr_mim,fingpr_usr)
                    currgame.points += score
                    print('\nYour score for that mimic: ',score)
                    print('\nTotal points collected so far: ',currgame.points)
                else:
                    print("Thanks for playing!")
                    currgame.points = max_points
                    currgame.close_game()
            if currgame.cont_game:
                print("\nCongratulations!!! You're a MIMIC MASTER!!")
            currgame.cont_game = False
            currgame.close_game()