#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 16:14:17 2018

Goal: trying to mimic what Audacity does in noise reduction
https://wiki.audacityteam.org/wiki/
Using same FFT window size as Audacity: 2048
Which leads to 1025 frequency bands

Other research using fft to capture speech features have used 25ms windows w 10ms window shifts

#with scipy.signal.istft I am having issues maintaining 25ms windows w 10 ms shifts... for now leaving out NFFT = 2048, and using 50ms windows instead. COLA constraints have failed otherwise. Will continue working on that tho... in the future

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

def load_wave(wavefile):
    y, sr = librosa.load(wavefile)
    return y,sr

def wave2stft(wavefile):
    y, sr = librosa.load(wavefile)
    if len(y)%2 != 0:
        y = y[:-1]
    #nperseg = int(sr*0.05)
    #f,t,stft = signal.stft(y,sr,nperseg = None)
    stft = librosa.stft(y)
    stft = np.transpose(stft)
    return stft, y, sr

def stft2wave(stft,len_origsamp):
    #get num bandwidths... with this COLA constraints get satisfied for istft
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.istft.html
    #nperseg = stft.shape[1]
    #nperseg = int(sr*0.5)
    #3/4 works well with Hanning window, and satisfies COLA constraints
    #noverlap = int(nperseg*(3/4))
    istft = np.transpose(stft.copy())
    #f,samples = signal.istft(istft,fs = sr,nperseg=nperseg)
    samples = librosa.istft(istft,length=len_origsamp)
    return samples

def stft2power(stft_matrix):
    stft = stft_matrix.copy()
    power = stft**2
    return(power)
    
def stft2amp(stft_matrix):
    stft = stft_matrix.copy()
    amp = np.abs(stft)
    return amp

def get_pitch(wavefile):
    y, sr = librosa.load(wavefile)
    if len(y)%2 != 0:
        y = y[:-1]
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

def get_rms(matrix_bandwidths):
    bw = matrix_bandwidths.copy()
    bw = np.sqrt(sum(bw**2)/len(bw))
    return bw

def get_var_bandwidths(matrix_bandwidths):
    bw = matrix_bandwidths.copy()
    bw_var = [np.var(bw[:,bandwidth]) for bandwidth in range(bw.shape[1])]
    return bw_var

def rednoise(noise_powerspec_mean,noise_powerspec_variance, speech_powerspec_row,speech_stft_row):
    npm = noise_powerspec_mean
    npv = noise_powerspec_variance
    spr = speech_powerspec_row
    stft_r = speech_stft_row.copy()
    for i in range(len(spr)):
        if spr[i] <= npm[i] + npv[i]:
            stft_r[i] = 1e-3
    return stft_r

#def rednoise(noise_powerspec_mean,noise_powerspec_variance, speech_powerspec_row,speech_stft_row):
    #npm = noise_powerspec_mean
    #npv = noise_powerspec_variance
    #spr = speech_powerspec_row
    #stft_r = speech_stft_row.copy()
    #for i in range(len(spr)):
        #if spr[i] <= npm[i] + npv[i]:
            #stft_r[i] = 1e-3
    #return stft_r
    
    
def matchvol(target_powerspec, speech_powerspec, speech_stft):
    tmp = np.max(target_powerspec)
    smp = np.max(speech_powerspec)
    stft = speech_stft.copy()
    if smp > tmp:
        mag = tmp/smp
        stft *= mag
    return stft
        
def savewave(filename,samples,sr):
    librosa.output.write_wav(filename,samples,sr)
    print("File has been saved")

def power2stft(power_spec):
    stft = np.sqrt(power_spec)
    return stft

def get_lengthwave(samples,sr):
    len_sec = len(samples)/float(sr)
    return len_sec

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

def voice_onset_index(stft, stft_powermean, stft_var):
    for row in range(len(stft)):
        if sum(np.abs(stft[row])) > sum(stft_powermean + stft_var):
            if row < len(stft) - 3:
                if sum(np.abs(stft[row+1])) and sum(np.abs(stft[row+2])) and  sum(np.abs(stft[row+3])) > sum(stft_powermean + stft_var):
                    return row 
        else:
            print("No speech detected")
    return None
                    
    

