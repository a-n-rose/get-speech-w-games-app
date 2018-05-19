#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 19 13:47:06 2018

@author: airos
"""

import acoustid
import chromaprint
import sounddevice as sd
import soundfile as sf
import pygame
from fuzzywuzzy import fuzz
import datetime

class Comp_FP:
    def __init__(self, file1, file2):
        self.date = datetime.datetime.now()
        self.file1 = file1
        self.file2 = file2
    
    def get_fp(self,filename):
        duration, fp_encoded = acoustid.fingerprint_file(filename)
        fingerprint, version = chromaprint.decode_fingerprint(fp_encoded)
        return(fingerprint)
        
    def record_user(self,duration):
        recording = False
        while recording == False:
            print("Now recording :P")
            recording = True
        duration = duration
        fs = 44100
        user_rec = sd.rec(int(duration*fs),samplerate=fs,channels=2)
        sd.wait()
        return user_rec
    
    def play_rec(self, recording):
        fs = 44100
        sd.play(recording, fs)
        sd.wait()
        return None
    
    def save_rec(self,filename,rec,fs):
        sf.write(filename,rec,fs)
        print('file was saved!')
        return None
    
    def play_wav(self,filename):
        pygame.init()
        sound = pygame.mixer.Sound(filename)
        sound.play()
        while pygame.mixer.get_busy():
            pass
        return None
    
    def comp_fp(self,fingerprint1,fingerprint2):
        similarity = fuzz.ratio(fingerprint1,fingerprint2)
        return(similarity)
    
    def close_prog(self):
        '''
        close and save anything that was open during the game
        '''
        pygame.quit()
