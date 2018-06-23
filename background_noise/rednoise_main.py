#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 21:02:09 2018

@author: airos
"""

import librosa
import numpy as np
import matplotlib.pyplot as plt

from rednoise_fun import rednoise, wave2stft, stft2power, get_mean_bandwidths, get_var_bandwidths, stft2wave, savewave, get_date, matchvol, get_pitch, get_pitch_mean, load_wave, pitch_sqrt


noise = 'Aislyn_2018_20_12_10__3.wav'
speech = 'Aislyn_2018_20_12_54__27.wav'
owl = 'dove-Mike_Koenig-1208819046_orig.wav'

n_stft,nsr = wave2stft(noise)
sp_stft,spsr = wave2stft(speech)
owl_stft,osr = wave2stft(owl)

n_power = stft2power(n_stft)
sp_power = stft2power(sp_stft)
o_power = stft2power(owl_stft)

npow_m = get_mean_bandwidths(n_power)
npow_v = get_var_bandwidths(n_power)

sp_stftred = np.array([rednoise(npow_m,npow_v,sp_power[i],sp_stft[i]) for i in range(sp_stft.shape[0])])

wave_sample = stft2wave(sp_stftred,spsr)
date = get_date()
savewave('rednoise_{}.wav'.format(date),wave_sample,spsr)

#now match volume/max power
sp_stftmatched = matchvol(o_power,sp_power,sp_stftred)
wave_sample2 = stft2wave(sp_stftmatched,spsr)
date = get_date()
savewave('rednoise2_{}.wav'.format(date),wave_sample2,spsr)


speech_red1 = 'rednoise_2018y6m23d22h19m55s.wav'
speech_red2 = 'rednoise2_2018y6m23d22h19m55s.wav'
noise_samp, nsr = load_wave(noise)
sp1,spsr1 = load_wave(speech)
sp2,spsr2 = load_wave(speech_red1)
sp3,spsr3 = load_wave(speech_red2)
o_samp, osr = load_wave(owl)

#compare pitch curves:
#get pitch
npitch,nm = get_pitch(noise_samp,nsr)
sp1pitch, sp1m = get_pitch(sp1,spsr1)
sp2pitch, sp2m = get_pitch(sp2,spsr2)
sp3pitch, sp3m = get_pitch(sp3,spsr3)
opitch,om = get_pitch(o_samp,ospr)
#get mean pitch
np_mean = get_pitch_mean(npitch)
sp1p_mean = get_pitch_mean(sp1pitch)
sp2p_mean = get_pitch_mean(sp2pitch)
sp3p_mean = get_pitch_mean(sp3pitch)
op_mean = get_pitch_mean(opitch)
#square root means
npm_sqrt = pitch_sqrt(np_mean)
sp1pm_sqrt = pitch_sqrt(sp1p_mean)
sp2pm_sqrt = pitch_sqrt(sp2p_mean)
sp3pm_sqrt = pitch_sqrt(sp3p_mean)
opm_sqrt = pitch_sqrt(op_mean)


#plots!!
plt.plot(npm_sqrt)
plt.plot(sp1pm_sqrt)
plt.plot(sp2pm_sqrt)
plt.plot(sp3pm_sqrt)
plt.plot(opm_sqrt)
