import os
import pygame

''' Audio Module - Handles laoding and playing sound effects safely '''

# load sound
def load_sound(filename):
    ''' Loads a sound file from the sounds directory
    and returns pygame.mixer.Sound object if file exists,
    otherwise, None '''
    
    # builds path relative to project structure 
    path = os.path.join(os.path.dirname(__file__), "..", "sounds", filename)

    # checks if file exists before loading 
    if os.path.exists(path):
        try:
            return pygame.mixer.Sound(path)
        except pygame.error:
            return None

    # fallback if file missing 
    return None

# play sound 
def play_sound(sound):
    '''Safely plays a sound if it exists, 
    prevents crashes when sound is None '''
    
    if sound:
        sound.play()