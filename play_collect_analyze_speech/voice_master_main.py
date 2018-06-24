#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 15 22:22:15 2018

@author: airos
"""
import numpy as np

from rednoise_run import wave2pitchmeansqrt
from voice_master import Mimic_Game
import os

#import shutil
   
   
def compare_sim(pitch_mean1, pitch_mean2):
    pm1 = pitch_mean1.copy()
    pm2 = pitch_mean2.copy()
    if len(pm1) != len(pm2):
        index_min = np.argmin([len(pm1),len(pm2)])
        if index_min > 0:
            pm1 = pm1[:len(pm2)]
        else:
            pm2 = pm2[:len(pm1)]
    corrmatrix = np.corrcoef(pm1,pm2)
    return(corrmatrix)
   

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
#        print("\n\nDuring the next step, we need you stay as quiet as you can - we need to measure the background noise for {} seconds.\n\n".format(sec))
        
        #have to figure out how to use the silence to cancel out background noise
        print("\nThis next step will take just {} seconds\n".format(sec))
        test_mic = currgame.start_game('test your mic')
        if test_mic:
            print("Now recording. Please stay quiet as we measure the background noise.")
        mictest = currgame.test_mic(sec)
        if mictest == False:
            print("We couldn't test your mic..")
        while currgame.cont_game == True:
            while currgame.points < max_points:
                currgame.cont_game = currgame.start_game('listen to a sound')
                if currgame.cont_game:
                    print("Right after this plays, we will record your attempt at the sound. Get ready!")
                    mim_filename = directory_mim+currgame.rand_sound2mimic()
                    duration = currgame.get_duration(mim_filename)
                    #max_amp = currgame.get_max_amp(mim_filename)
                    rep_mim = currgame.record_user(duration)

                    #save the recording
                    time_str = currgame.get_date()
                    usr_recfilename = directory_user+username+'_'+time_str+'.wav'
                    currgame.save_rec(usr_recfilename,rep_mim,fs=22050)
                    
                    #subtract noise, match target recording
                    # get and compare pitch means (sqrt)
                    pitchsqrt_speech,pitchsqrt_target,pitchsqrt_noise = wave2pitchmeansqrt(usr_recfilename,mim_filename,currgame.noisefile)
                    
                    #compare similarities
                    sp2noise = compare_sim(pitchsqrt_speech,pitchsqrt_noise)
                    sp2target = compare_sim(pitchsqrt_speech,pitchsqrt_target)
                    
                    score_noise = sum(sum(sp2noise))
                    score_target = sum(sum(sp2target))
                    
                    score = score_target/score_noise
                    points = int(score**10) * 10
                    if score > 1:
                        print("Not bad! You earned {} points.".format(points))
                    else:
                        print("You call that a mimic? No points earned. Try again!")
                        
                    currgame.points += points
                else:
                    print("Thanks for playing!")
                    currgame.points = max_points
                    currgame.close_game()
            if currgame.cont_game:
                print("\nCongratulations!!! You're a MIMIC MASTER!!")
            currgame.cont_game = False
            currgame.close_game()
            #shutil.rmtree(directory_user)
            
