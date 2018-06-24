#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 16:14:17 2018

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

def load_wave(wavefile):
    #y, sr = librosa.load(wavefile, sr=None)
    y, sr = librosa.load(wavefile)
    return y,sr

def wave2stft(wavefile):
    #y, sr = librosa.load(wavefile,sr=None)
    y, sr = librosa.load(wavefile)
    if len(y)%2 != 0:
        y = y[:-1]
    #hop = int(sr*0.01)
    nperseg = int(sr*0.05)
    #noverlap = nperseg - hop
    #f,t,stft = signal.stft(y,sr,nperseg = nperseg,noverlap=noverlap)
    f,t,stft = signal.stft(y,sr,nperseg = nperseg)
    stft = np.transpose(stft)
    return stft, sr

def stft2wave(stft,sr):
    #hop = int(sr*0.01)
    nperseg = int(sr*0.05)
    #noverlap = nperseg - hop
    istft = np.transpose(stft.copy())
    f,samples = signal.istft(istft,fs=sr,nperseg=nperseg)
    return samples

def stft2power(stft_matrix):
    stft = stft_matrix.copy()
    power = np.abs(stft)**2
    return(power)
    
def stft2amp(stft_matrix):
    stft = stft_matrix.copy()
    amp = np.abs(stft)
    return amp

def get_pitch(wavefile):
    #y,sr = librosa.load(wavefile, sr=None)
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
