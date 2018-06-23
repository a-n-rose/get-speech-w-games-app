
import matplotlib.pyplot as plt
import numpy as np

from rednoise_fun import wave2stft, stft2power, stft2amp, get_mean_bandwidths, rednoise, stft2wave, savewave, get_var_bandwidths, get_date

if __name__ == '__main__':
    noise_file = 'Aislyn_2018_20_12_10__3.wav'
    speech_file = 'Aislyn_2018_20_12_54__27.wav'
    
    #subtract noise 
    
    #get stft and sampling rage
    noise_stft, noise_sr = wave2stft(noise_file)
    speech_stft, speech_sr = wave2stft(speech_file)
    
    #get amplitude
    noise_amp = stft2amp(noise_stft)
    sp_amp = stft2amp(speech_stft)
    #get mean amplitude (for each bandwidth)
    noise_amp_mean = get_mean_bandwidths(noise_amp)
    #get amplitude variance
    noise_amp_var = get_var_bandwidths(noise_amp)
    
    #subtract noise from power and stft
#    start_col = 215
#    col_len = 30
#    stft_red_100 = rednoise_short(noise_pw_mean,sp_amp[100],speech_stft[100],start_col,col_len) 
    stft_red = [rednoise(noise_amp_mean,noise_amp_var,sp_amp[row],speech_stft[row]) for row in range(speech_stft.shape[0])]
    
    #transform stft back to wave
    speech_red = stft2wave(stft_red,speech_sr)
    date = get_date()
    savewave("rednoise_{}.wav".format(date),speech_red,speech_sr)
    

    


    
    

    
