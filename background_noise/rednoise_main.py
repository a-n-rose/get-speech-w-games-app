#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 21:02:09 2018

@author: airos
"""

import librosa
import numpy as np

from rednoise_fun import rednoise, wave2stft, stft2power, get_mean_bandwidths, get_var_bandwidths, stft2wave, savewave, get_date


noise = 'Aislyn_2018_20_12_10__3.wav'
speech = 'Aislyn_2018_20_12_54__27.wav'
owl = 'dove-Mike_Koenig-1208819046_orig.wav'

n,nsr = wave2stft(noise)
sp,spsr = wave2stft(speech)
owl,owlsr = wave2stft(owl)

n_power = stft2power(n)
sp_power = stft2power(sp)

npow_m = get_mean_bandwidths(n_power)
npow_v = get_var_bandwidths(n_power)

sp_stftred = np.array([rednoise(npow_m,npow_v,sp_power[i],sp[i]) for i in range(sp.shape[0])])

wave_sample = stft2wave(sp_stftred,spsr)
date = get_date()
savewave('rednoise_{}.wav'.format(date),wave_sample,spsr)
