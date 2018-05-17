 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 14 16:13:28 2018

@author: airos
"""

import sounddevice as sd

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
        self.user_name = None
        
    def enter_username(self):
        username = input("Please enter your username: ")
        if username:
            return username
        else:
            self.enter_username()
    
    def start_game(self):
        user_ready = input("Press ENTER to start or type 'exit' to leave: ")
        if user_ready == '':
            print("Great!")
            username = self.enter_username()
            return username
        elif 'exit' in user_ready.lower():
            return None
        else:
            self.start_game()
    
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
        ready2test = input("Ready to test your mic?\n \nIf yes, we will record for {} seconds and play the recording immediately afterwards.\n \nType 'yes' or 'no': ".format(str(sec)))
        if 'n' in ready2test:
            return False
        elif 'y' in ready2test:
            user_rec = self.test_record()
            if user_rec.any():
                print("\nFinished recording.\n \nHere's what you sounded like:")
                self.play_rec(user_rec)
                return True
            else:
                print("Hmmmmm.. something went wrong. Check your mic and try again.")
                self.test_mic(sec)
                
        else:
            print("\n \n \n \n")
            print("\n** Please enter either 'y' or 'n' **".upper())
            self.test_mic(sec)