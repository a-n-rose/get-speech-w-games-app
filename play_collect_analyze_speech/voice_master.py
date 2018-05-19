 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 14 16:13:28 2018

@author: airos
"""

import sounddevice as sd
import random
import glob
import os
import pygame


class Mimic_Game:
    def __init__(self):
        print(
                '''
                Welcome to the game: I CAN MIMIC THAT!
                
                We will present to you sounds and you must try to sound as much like them as you can. 
                
                The better you are, the more points you collect.
                
                If you earn 100 points, you will be titled
                MIMIC MASTER
                                
                '''
                )
        self.username = None
        self.cont_game = True
        
        
    def enter_username(self):
        username = input("Please enter your username: ")
        if username:
            return username
        else:
            self.enter_username()
    
    def start_game(self,action,username = None):
        user_ready = input("Press ENTER to {} or type 'exit' to leave: ".format(action))
        if user_ready == '':
            if username:
                print("Great!")
                self.username = self.enter_username()
                return self.username
            else:
                return True
        elif 'exit' in user_ready.lower():
            return False
        else:
            self.start_game('start')
    
    def record_user(self,duration):
        duration = duration
        fs = 44100
        user_rec = sd.rec(int(duration*fs),samplerate=fs,channels=2)
        sd.wait()   
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
        sd.wait()
        return None
    
    def test_record(self):
        '''
        The user will need to do a test record to analyze natural voice.
        Perhaps read a sentence aloud?
        '''

        user_rec = self.record_user(2)

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
    
    def test_mic(self,sec):
        user_rec = self.test_record()
        sd.wait()
        if user_rec.any():
            sd.wait()
            print("This is what you sounded like!")
            self.play_rec(user_rec)
            sd.wait()
        else:    
            print("Hmmmmm.. something went wrong. Check your mic and try again.")
            if self.start_game('test your mic'):
                self.test_mic(5)
            else:
                return False
     
    def rand_sound2mimic(self):
        os.chdir('./soundfiles/')
        try:
            sounds = [wave for wave in glob.glob('*.wav')]
            rand_ind = random.randint(0,len(sounds)-1)
            filename = sounds[rand_ind]
            pygame.init()
            rand_sound = pygame.mixer.Sound(filename)
            rand_sound.play()
            while pygame.mixer.get_busy():
                pass
            print("Start mimicking!")
        except ValueError:
            print("Value Error!")
        finally:
            os.chdir('..')
        return None
    
    def close_game(self):
        '''
        close and save anything that was open during the game
        '''
        pygame.quit()
        
