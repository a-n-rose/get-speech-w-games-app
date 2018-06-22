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


def stft(sig, frameSize, overlapFac=0.60, window=np.hanning):
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



#based off of Audacity
NFFT = 2048



#looking at recorded background noise
bgnd_file = "Aislyn_2018_20_12_10__3.wav"
bgnd, bgsr = librosa.load(bgnd_file,sr=None)
bgnd_stft = stft(bgnd,NFFT)
bgnd_power = np.abs(bgnd_stft)**2
#num of frequency bandwidths:
bgnd_bw = bgnd_power.shape[1]
#collect power means of all bandwidths
bgnd_bw_mean = [np.mean(bgnd_power[:,bandwidth]) for bandwidth in range(bgnd_bw)]

#compare with noisy speech sample (matched environment)
sp_file = "Aislyn_2018_20_12_54__27.wav"
sp, spsr = librosa.load(sp_file,sr=None)
sp_stft = stft(sp,NFFT)
sp_power = np.abs(sp_stft)**2
#num freq bandwidths:
sp_bw = sp_power.shape[1]
#collect power means of bandwidths
sp_bw_mean = [np.mean(sp_power[:,bandwidth]) for bandwidth in range(sp_bw)]
sp_bw_mean

#compare with ideal sound (no noise, good amplitude):
owl_file = 'dove-Mike_Koenig-1208819046_orig.wav'
owl, owlsr = librosa.load(owl_file,sr=None)
owl_stft = stft(owl,NFFT)
owl_power = np.abs(owl_stft)**2
#num bandwidths:
owl_bw = owl_power.shape[1]
owl_bw_mean = [np.mean(owl_power[:,bandwidth]) for bandwidth in range(owl_bw)]

#just checking to see how many of these mean sets are greater than 1:
bgnd_nparray = np.array(bgnd_bw_mean)
sum(bgnd_nparray)   #115710.66060362234
sp_nparray = np.array(sp_bw_mean)
sum(sp_nparray)   #542385.5694168168
owl_nparray= np.array(owl_bw_mean)
sum(owl_nparray > 1)  #49
#Okay... big difference here... 







