## Mimic Game

voice_master_main.py
voice_master.py
(need thinkdsp.py and thinkplot.py in same directory)

This is a simple game where the user is presented sounds to mimic (i.e. animals) and earns points based on how well they mimic the sound.
* I collected some bird sounds from here: http://soundbible.com/tags-bird.html

So far I have collected some bird sounds and built scripts that play them and record the user (based on the duration of the target sound)
I also have implemented Chromaprint via pyacoustid; doesn't really seem to work yet. Maybe noise and onset differences? The game also keeps track of the points collected and stops once the user collects a certain amount.

Next steps include managing noisy speech data and basically making the fingerprint comparison worthwhile


