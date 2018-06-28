#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 17:27:24 2018

This code doesn't quite work but I did find the 
indices of where sound starts and ends which is
relevant for comparing pitch curves. Apply this
to the pitch analysis and can then compare the 
curve areas of interest and also match them up! 


@author: airos
"""
import os
import glob

import librosa
import numpy as np
import datetime



def wave2stft(wavefile):
    y, sr = librosa.load(wavefile)
    if len(y)%2 != 0:
        y = y[:-1]
    stft = librosa.stft(y)
    #n_fft = 2048
    #n = len(y)
    #y_pad = librosa.util.fix_length(y,n+n_fft//2)
    #stft = librosa.stft(y_pad,n_fft = n_fft)
    stft = np.transpose(stft)
    return stft, y, sr

def stft2wave(stft,len_origsamp):
    istft = np.transpose(stft.copy())
    samples = librosa.istft(istft,length=len_origsamp)
    return samples

def get_energy(stft_matrix):
    #stft.shape[1] == bandwidths/frequencies
    #stft.shape[0] pertains to the time domain
    rms_list = [np.sqrt(sum(np.abs(stft_matrix[row])**2)/stft_matrix.shape[1]) for row in range(len(stft_matrix))]
    return rms_list

def get_energy_mean(energy_list):
    mean = sum(energy_list)/len(energy_list)
    return mean


def suspended_energy(rms_speech,row,rms_mean_noise,start):
    if start == True:
        if rms_speech[row+1] and rms_speech[row+2] > rms_mean_noise:
            return True
    else:
        if rms_speech[row-1] and rms_speech[row-2] > rms_mean_noise:
            return True


def sound_index(rms_speech, start = True, rms_mean_noise = None):
    if rms_mean_noise == None:
        rms_mean_noise = 1
    if start == True:
        side = 1
        start = 0
        end = len(rms_speech)
    else:
        side = -1
        start = len(rms_speech)-1
        end = -1
    for row in range(start,end,side):
        if rms_speech[row] > rms_mean_noise:
            if suspended_energy(rms_speech,row,rms_mean_noise,start):
                if start:
                    #to catch plosive sounds
                    while row >= 0:
                        row += 1
                        row += 1
                        break
                    return row
                else:
                    #to catch quiet cronsonant endings
                    while row <= len(rms_speech):
                        row -= 1
                        row -= 1
                        break
                    return row
    else:
        print("No speech detected.")
    return None

def get_date():
    time = datetime.datetime.now()
    time_str = "{}y{}m{}d{}h{}m{}s".format(time.year,time.month,time.day,time.hour,time.minute,time.second)
    return(time_str)

def savewave(filename,samples,sr):
    librosa.output.write_wav(filename,samples,sr)
    print("File has been saved")




if __name__ == '__main__':
    directory_newfiles = './soundfiles/clipped/'
    if not os.path.exists(directory_newfiles):
        os.makedirs(directory_newfiles)
    for wav in glob.glob("soundfiles/*.wav"):
        stft,y,sr = wave2stft(wav)
        energy = get_energy(stft)
        #find where sound starts:
        sound_start = sound_index(energy)
        sound_end = sound_index(energy,start=False)
        stft_red = stft[sound_start:sound_end]
        start_ratio = sound_start/len(energy)
        end_ratio = sound_start/len(energy)
        start_sample = int(len(y)*start_ratio)
        end_sample = int(len(y)*end_ratio)
        new_length = end_sample - start_sample
        #y_red = stft2wave(stft_red,new_length)
        y_red = y[start_sample:end_sample]
        date = get_date()
        wavefile = wav[11:]
        wavefile_name = wavefile[:-4]
        saved_name = "{}{}_{}.wav".format(directory_newfiles,wavefile_name,date)
        savewave(saved_name,y_red,sr)