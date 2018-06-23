#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 16:14:17 2018

Pulled code from: https://github.com/zhr1201/Multi-channel-speech-extraction-using-DNN/blob/master/multichannel_cnn/audio_eval.py
~ def stft()

Goal: trying to mimic what Audacity does in noise reduction
https://wiki.audacityteam.org/wiki/
Using same FFT window size as Audacity: 2048
Which leads to 1025 frequency bands

Other research using fft to capture speech features have used 25ms windows w 10ms window shifts

@author: airos
"""


import numpy as np
from numpy.lib import stride_tricks
import librosa
from scipy import signal
import datetime

def get_date():
    time = datetime.datetime.now()
    time_str = "{}y{}m{}d{}h{}m{}s".format(time.year,time.month,time.day,time.hour,time.minute,time.second)
    return(time_str)


#2048 based off of Audacity
def stft(sig, frameSize= 2048, overlapFac=0.60, window=np.hanning):
    """ short time fourier transform of audio signal """
    win = window(frameSize)
    hopSize = int(frameSize - np.floor(overlapFac * frameSize))
    # zeros at beginning (thus center of 1st window should be for sample nr. 0)
    # samples = np.append(np.zeros(np.floor(frameSize / 2.0)), sig)
    samples = np.array(sig, dtype='float64')
    # cols for windowing
    cols = np.ceil((len(samples) - frameSize) / float(hopSize)) + 1
    # zeros at end (thus samples can be fully covered by frames)
    # samples = np.append(samples, np.zeros(frameSize))
    frames = stride_tricks.as_strided(
        samples,
        shape=(int(cols), frameSize),
        strides=(samples.strides[0] * hopSize, samples.strides[0])).copy()
    frames *= win
    return np.fft.rfft(frames)

def wave2stft(wavefile):
    y, sr = librosa.load(wavefile,sr=None)
    f,t,stft = signal.stft(y,sr,nperseg = int(sr*0.025),nfft=2048)
    stft = np.transpose(stft)
    return stft, sr

def stft2power(stft_matrix):
    stft = stft_matrix.copy()
    power = np.abs(stft)**2
    return(power)
    
def stft2amp(stft_matrix):
    stft = stft_matrix.copy()
    amp = np.abs(stft)
    return amp

def get_pitch(y,sr):
    pitches,mag = librosa.piptrack(y=y,sr=sr)
    return pitches,mag

def get_pitch_mean(matrix_pitches):
    p = matrix_pitches.copy()
    p_mean = [np.mean(p[:,time_unit]) for time_unit in range(p.shape[1])]
    p_mean = np.transpose(p_mean)
    #remove beginning artifacts:
    pmean = p_mean[int(len(p_mean)*0.07):]
    return pmean
              
def pitch_sqrt(pitch_mean):
    psqrt = np.sqrt(pitch_mean)
    return psqrt
    
def get_mean_bandwidths(matrix_bandwidths):
    bw = matrix_bandwidths.copy()
    bw_mean = [np.mean(bw[:,bandwidth]) for bandwidth in range(bw.shape[1])]
    return bw_mean

def get_var_bandwidths(matrix_bandwidths):
    bw = matrix_bandwidths.copy()
    bw_var = [np.var(bw[:,bandwidth]) for bandwidth in range(bw.shape[1])]
    return bw_var
                                                               
#def red_noise(noise_powerspec_mean,speech_powerspec_row, ):
    #npm = noise_powerspec_mean
    #spr = speech_powerspec_row.copy()
    #for i in range(len(spr)):
        #if spr[i] <= npm[i]:
            #spr[i] = 1e-6
        #else:
            #diff = spr[i] - npm[i]
            #spr[i] = diff
    #return spr

def rednoise_short(noise_powerspec_mean, speech_powerspec_row,speech_stft_row, col_start,col_len):
    npm = noise_powerspec_mean[col_start:col_start+col_len]
    spr = speech_powerspec_row[col_start:col_start+col_len]
    stft_r = speech_stft_row[col_start:col_start+col_len].copy()
    for i in range(len(spr)):
        print(stft_r[i])
        if spr[i] <= npm[i]:
            stft_r[i] = 1e-3
        else:
            print(spr[i])
            print(npm[i])
            mag = npm[i]/float(spr[i])
            print(mag)
            stft_r[i] *= mag
            print(stft_r[i])
    return stft_r

def rednoise(noise_powerspec_mean,noise_powerspec_variance, speech_powerspec_row,speech_stft_row):
    npm = noise_powerspec_mean
    npv = noise_powerspec_variance
    spr = speech_powerspec_row
    stft_r = speech_stft_row.copy()
    for i in range(len(spr)):
        if spr[i] <= npm[i] + npv[i]:
            stft_r[i] = 1e-3
        else:
            mag = npm[i]/float(spr[i])
            stft_r[i] *= mag
    return stft_r
#
#def red_noise(noise_powerspec_mean, speech_powerspec_row,speech_stft_row):
#    npm = noise_powerspec_mean
#    spr = speech_powerspec_row
#    stft_r = speech_stft_row.copy()
#    for i in range(len(spr)):
#        if spr[i] <= npm[i]:
#            stft_r[i] = 1e-3
#        else:
#            mag = npm[i]/float(spr[i])
#            stft_r[i] *= np.sqrt(mag)
#    return stft_r
#            
    

def stft2wave(stft,sr):
    istft = np.transpose(stft.copy())
    f,samples = signal.istft(istft,fs=sr,nperseg=int(sr*0.025),nfft=2048)
    return samples

def savewave(filename,samples,sr):
    librosa.output.write_wav(filename,samples,sr)
    print("File has been saved")

                                                        
def power2stft(power_spec):
    stft = np.sqrt(power_spec)
    return stft

def get_lengthwave(samples,sr):
    len_sec = len(samples)/float(sr)
    return len_sec



    



















