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

def stft2power(stft_matrix):
    stft = stft_matrix.copy()
    power = np.abs(stft)**2
    return(power)
    
def stft2amp(stft_matrix):
    stft = stft_matrix.copy()
    amp = np.abs(stft)
    return amp

def get_energy(matrix_bandwidths):
    rms_list = [np.sqrt(sum(np.abs(matrix_bandwidths[row])**2)/matrix_bandwidths.shape[1]) for row in range(len(matrix_bandwidths))]
    return rms_list

def get_energy_mean(rms_list):
    mean = sum(rms_list)/len(rms_list)
    return mean

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


def suspended_energy(rms_speech,row,rms_mean_noise,start):
    if start == True:
        if rms_speech[row+1] and rms_speech[row+2] > rms_mean_noise:
            return True
    else:
        if rms_speech[row-1] and rms_speech[row-2] > rms_mean_noise:
            return True


def voice_index(rms_speech,rms_mean_noise = None, start = True):
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
                    return row-1
                else:
                    #to catch quiet consonant endings
                    return row+1
    else:
        print("No speech detected.")
    return None

        
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
