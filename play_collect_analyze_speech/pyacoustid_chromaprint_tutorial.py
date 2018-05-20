#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 19 12:38:10 2018

I pulled basic examples from on-line somewhere... but I implemented them here comparing a file (on local device) with a "live" recording
"""

import acoustid
import chromaprint
import sounddevice as sd
import soundfile as sf
import pygame
from fuzzywuzzy import fuzz


#example of fingerprint w chromaprint
duration, fp_encoded = acoustid.fingerprint_file('dove-Mike_Koenig-1208819046.wav')
fingerprint, version = chromaprint.decode_fingerprint(fp_encoded)
print(fingerprint)

#plotting the fingerprint
import numpy as np
import matplotlib.pyplot as plt
plt.figure()
bitmap = np.transpose(np.array([[b=='1' for b in list('{:32b}'.format(i & 0xffffffff))]for i in fingerprint]))
plt.imshow(bitmap)

pygame.quit()


#check similarity with another file

#first create new wave file (user mimics the sound)
def record_user(duration):
    duration = duration
    fs = 44100
    user_rec = sd.rec(int(duration*fs),samplerate=fs,channels=2)
    sd.wait()
    return user_rec

def play_rec(recording):
    fs = 44100
    sd.play(recording, fs)
    sd.wait()
    return None

def save_rec(filename,rec,fs):
    sf.write(filename,rec,fs)
    print('file was saved!')
    return None
       
#play sound to mimic
pygame.init()
sound2mimic = pygame.mixer.Sound('dove-Mike_Koenig-1208819046.wav')
sound2mimic.play()

#record user mimicking the sound
rec = record_user(5)
play_rec(rec)        
save_rec('usr_mimic.wav',rec,fs=44100)


#create fingerprints for mimicked sound and mimic:
duration1, fp_encoded1 = acoustid.fingerprint_file('dove-Mike_Koenig-1208819046.wav')
fingerprint1, version1 = chromaprint.decode_fingerprint(fp_encoded1)
print(fingerprint1)

duration_mim, fp_encoded_mim = acoustid.fingerprint_file('usr_mimic.wav')
fingerprint_mim, version_mim = chromaprint.decode_fingerprint(fp_encoded_mim)
print(fingerprint_mim)

#compare the sounds!
similarity_mim = fuzz.ratio(fingerprint_mim,fingerprint1)

#anc compare with totally non-mimicked wave file:
rec = record_user(5)
play_rec(rec)        
save_rec('usr_no_mimic.wav',rec,fs=44100)

duration_no_mim, fp_encoded_no_mim = acoustid.fingerprint_file('usr_no_mimic.wav')
fingerprint_no_mim, version_no_mim = chromaprint.decode_fingerprint(fp_encoded_no_mim)
print(fingerprint_no_mim)

similarity_no_mim = fuzz.ratio(fingerprint_no_mim,fingerprint1)



#Didn't work at all... 
#maybe need to process the noise...
