 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 14 16:13:28 2018

@author: airos
"""

import sounddevice as sd

class Mimic_Game:
    def __init__(self,user_name):
        print(
                '''
                Welcome to the WHAT YOUR VOICE CAN SOUND LIKE game
                
                We will present to you sounds to mimic. 
                
                The more you can make your voice sound like what we play
                the more points you collect.
                
                If you earn 100 points, you will be titled
                {}, THE VOICE MASTER
                
                '''.format(user_name.upper())
                )
        self.user_name = user_name
        
    def record_user(self,duration):
        duration = duration
        fs = 44100
        user_rec = sd.rec(int(duration*fs),samplerate=fs,channels=2,blocking=True)
        return(user_rec)
    
    def check_rec(self,user_rec):
        '''
        Need to check the speech to make sure the recording was 
        successful and not too much background noise is there.
        '''
        if user_rec.any():
            return True
        return False
    
    def play_rec(self,recording):
        fs = 44100
        sd.play(recording, fs)
        return None
    
    def test_record(self):
        '''
        The user will need to do a test record to analyze natural voice.
        Perhaps read a sentence aloud?
        '''

        user_rec = self.record_user(5)

        if self.check_rec(user_rec):
        
            return user_rec
        else:
            print(
                    '''
                    Hmmmmmm there seems to be a problem.
                    Is your mic connected and/or activated?
                    
                    Sorry for the inconvenience.
                    '''
                    )
        
        return None
        