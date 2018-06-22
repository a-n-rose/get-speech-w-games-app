#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 16:14:17 2018

Pulled code from: https://github.com/zhr1201/Multi-channel-speech-extraction-using-DNN/blob/master/multichannel_cnn/audio_eval.py


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

background_noise_filename = "Aislyn_2018_20_12_10__3.wav"
backgroundnoise,sr = librosa.load(background_noise_filename,sr=None)

test_fft = stft(backgroundnoise,int(sr*0.025))
test_power_spec = np.abs(test_fft)**2
test_power_spec.shape

#compare with other files...
user_recording_filename = "Aislyn_2018_20_12_54__27.wav"
userrec, us_sr = librosa.load(user_recording_filename,sr=None)

user_fft = stft(userrec,int(sr*0.025))
user_power_spec = np.abs(user_fft)**2
user_power_spec.shape
