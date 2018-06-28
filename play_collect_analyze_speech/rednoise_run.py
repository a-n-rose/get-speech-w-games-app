import librosa
import numpy as np
import matplotlib.pyplot as plt

from rednoise_fun import rednoise, wave2stft, stft2power, get_mean_bandwidths, get_var_bandwidths, stft2wave, savewave, get_date, matchvol, get_pitch, get_pitch_mean, load_wave, pitch_sqrt, voice_onset_index, get_energy, get_energy_mean


def wave2pitchmeansqrt(wavefile, target, noise):
    y_stft, y, sr = wave2stft(wavefile)
    y_power = stft2power(y_stft)
    y_energy = get_energy(y_stft)
    n_stft, ny, nsr = wave2stft(noise)
    n_power = stft2power(n_stft)
    n_energy = get_energy(n_stft)
    n_energy_mean = get_energy_mean(n_energy)
    
    t_stft, ty, tsr = wave2stft(target)
    t_power = stft2power(t_stft)
    
    npow_mean = get_mean_bandwidths(n_power)
    #npow_mean = get_rms(n_power)
    npow_var = get_var_bandwidths(n_power)
    
    y_stftred = np.array([rednoise(npow_mean,npow_var,y_power[i],y_stft[i]) for i in range(y_stft.shape[0])])

    
    voice_start = voice_onset_index(y_energy,n_energy_mean)
    if voice_start:
        print(voice_start)
        print(voice_start/len(y_energy))
        start = voice_start/len(y_energy)
        start_time = (len(y)*start)/sr
        print("Start time: {} sec".format(start_time))
        y_stft_voice = y_stftred[voice_start:]
        voicestart_samp = stft2wave(y_stft_voice,len(y))
        date = get_date()
        savewave('rednoise_speechstart_{}.wav'.format(date),voicestart_samp,sr)
        print('Removed silence from beginning of recording. File saved.')
        
    else:
        #handle no speech in recording, or too much background noise
        pass
        
    
    rednoise_samp = stft2wave(y_stftred,len(y))
    date = get_date()
    savewave('rednoise_{}.wav'.format(date),rednoise_samp,sr)
    print('Background noise reduction complete. File saved.')
    print('Now matching volume to target recording.')
    
    y_stftmatched = matchvol(t_power,y_power,y_stftred)
    matchvol_samp = stft2wave(y_stftmatched,len(y))
    savewave('rednoise2_{}.wav'.format(date),rednoise_samp,sr)
    print('Matched volume. File saved.')
    print('Now extracting pitch information')
    
    y_pitch, y_m = get_pitch(wavefile)
    yp_mean = get_pitch_mean(y_pitch)
    ypm_sqrt = pitch_sqrt(yp_mean)
    
    n_pitch, n_m = get_pitch(noise)
    np_mean = get_pitch_mean(n_pitch)
    npm_sqrt = pitch_sqrt(np_mean)
    
    t_pitch, t_m = get_pitch(target)
    tp_mean = get_pitch_mean(t_pitch)
    tpm_sqrt = pitch_sqrt(tp_mean)
    return (ypm_sqrt, tpm_sqrt, npm_sqrt)
    
    
    
