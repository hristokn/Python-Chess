from random import randint
from view.component import Component
from game.custom_events import CustomEvent
from game.sound_player import SoundPlayer
from chess.enums import Color

SOUNDS = {
    'move1': 'sounds/standart/move1.mp3',
    'move2': 'sounds/standart/move2.mp3',
    'move3': 'sounds/standart/move3.mp3',
    'capture': 'sounds/standart/capture.mp3',
    'check': 'sounds/standart/check.mp3',
    'checkmate': 'sounds/standart/checkmate.mp3',
    'castle': 'sounds/standart/castle.mp3',
    'low_time': 'sounds/standart/low_time.mp3',
    'promote': 'sounds/standart/promote.mp3',
}

MOVE_SOUND_COUNT = 3

class ChessBoardSoundPlayer(Component):
    def __init__(self, sound_player: SoundPlayer, player_color: Color = None):
        super().__init__(0, 0, 0, '')
        self.priority = 0
        self.sound_player = sound_player
        self.player_color = player_color

    def draw(self, surface):
        pass

    def receive_event(self, event):
        if event.type == CustomEvent.PLAYED_MOVE.value:
            if getattr(event, 'is_checkmate', False):
                sound_key = 'checkmate'
            elif getattr(event, 'is_check', False):
                sound_key = 'check'
            elif getattr(event, 'is_promotion', False):
                sound_key = 'promote'
            elif getattr(event, 'is_capture', False):
                sound_key = 'capture'
            elif getattr(event, 'is_castle', False):
                sound_key = 'castle'
            else:
                sound_key = 'move' + str(randint(1, MOVE_SOUND_COUNT))

            if sound_key in SOUNDS:
                self.sound_player.play_sound(sound_key)

        elif event.type == CustomEvent.LOW_TIME.value and getattr(event, 'color', None) == self.player_color:
            sound_key = 'low_time'
            if sound_key in SOUNDS:
                self.sound_player.play_sound(sound_key)