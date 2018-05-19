#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 19 13:59:15 2018

@author: airos
"""

from comp_fingerprints import Comp_FP

if __name__ == '__main__':
    file1 = 'dove-Mike_Koenig-1208819046_orig.wav'
    file2 = None
    curr_fp = Comp_FP(file1,file2)
    
    if curr_fp.file2 == None:
        print("Try to mimic this sound:")
        curr_fp.play_wav(file1)
        print("Now recording!")
        usr_wav = curr_fp.record_user(5)
        curr_fp.file2 = 'usr_rec.wav'
        curr_fp.save_rec(curr_fp.file2,usr_wav,fs=44100)
        
    fp1 = curr_fp.get_fp(curr_fp.file1)
    fp2 = curr_fp.get_fp(curr_fp.file2)
    fp_sim = curr_fp.comp_fp(fp1,fp2)
    print(fp_sim)
    curr_fp.close_prog()