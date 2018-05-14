 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 14 16:13:28 2018

@author: airos
"""

class Game:
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
        
