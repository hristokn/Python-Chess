from pygame.mixer import Sound
from os.path import isfile

def loadSound(fileName):
    if isfile(fileName):
        sound = Sound(file=fileName)
        return sound
    else:
        raise Exception(f"Error loading sound: {fileName} – Check filename and path?")

class SoundPlayer:
    def __init__(self, sounds: dict[str, str]):
        self.sounds:dict[str, str] = sounds
        self.loaded_sounds:dict[str, Sound] = {}

    def __contains__(self, item):
        return item in self.sounds

    def __getitem__(self, item):
        if item not in self:
            raise KeyError
        try:
            return self.loaded_sounds[item]
        except KeyError:
            sound = loadSound(self.sounds[item])
            self.loaded_sounds[item] = sound
            return sound

    def play_sound(self, sound:str):
        self[sound].play()