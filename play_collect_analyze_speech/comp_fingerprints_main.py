#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 19 13:59:15 2018

@author: airos
"""

from comp_fingerprints import Comp_FP
import datetime
import librosa

class Context:
    def __init__(self,comp_name):
        self.comp_name = comp_name
        self.date = None


def get_duration(wavefile):
    y, fs = librosa.load(wavefile)
    print(fs)
    duration = len(y)/fs
    return(duration)

if __name__ == '__main__':
    comp_name = input("Name this fingerprint comparison: ")
    currcont = Context(comp_name)
    file1 = 'dove-Mike_Koenig-1208819046_orig.wav'
    file2 = None
    curr_fp = Comp_FP(file1,file2)
    
    if curr_fp.file2 == None:
        print("Try to mimic this sound:")
        curr_fp.play_wav(file1)
        print("Now recording!")
        duration = get_duration(file1)
        usr_wav = curr_fp.record_user(duration)
        time = datetime.datetime.now()
        time_str = "{}".format(str(time.year)+'_'+str(time.day)+'_'+str(time.hour)+'_'+str(time.minute))
        currcont.date = time_str
        file2 = 'usr_rec_{}.wav'.format(currcont.comp_name,currcont.date)
        curr_fp.file2 = file2
        curr_fp.save_rec(file2,usr_wav,fs=44100)
        
    fp1 = curr_fp.get_fp(curr_fp.file1)
    fp2 = curr_fp.get_fp(curr_fp.file2)
    fp_sim = curr_fp.comp_fp(fp1,fp2)
    print(fp_sim)
    print("First fingerprint {}:".format(file1))
    curr_fp.vis_fp(fp1)
    print("Second fingerprint {}:".format(file2))
    curr_fp.vis_fp(fp2)
    curr_fp.close_prog()