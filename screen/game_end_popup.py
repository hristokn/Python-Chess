from game.drawing import ImageLibrary
from game.mouse import Mouse
from screen.screen import Screen
from view.button import SmallTextButton
from view.text import Text
from view.image import Image
from game.custom_events import EventAnnouncer, post_event, CustomEvent
from chess.enums import Color 
from chess.finished_game import FinishedGame, VictoryType 
from game.sound_player import SoundPlayer 


class GameEndPopup(Screen):
    def __init__(self, mouse: Mouse, image_library: ImageLibrary, event_announcer: EventAnnouncer, 
                  sound_player: SoundPlayer, x, y,
                  color: Color, finished_game: FinishedGame, new_game_screen_name: str):
        super().__init__(mouse, image_library, event_announcer, sound_player, x, y, '')
        self.priority = 20
        self.new_game_screen_name = new_game_screen_name
        self.player_color = color
        
        text = ''
        if finished_game.victory_type == VictoryType.DRAW:
            text = 'Game ends in draw'
        elif finished_game.winner == self.player_color:
            text = 'You win!'
        else:
            text = 'You lost.'

        # popup 510 x 220
        # button 160 x 63
        # 30px button 130px button 30px
        # 127px button 30px
        #

        self.textbox: Text = Text(x, y, x + 510, y + 127, 5, image_library, text)
        self.add_element(self.textbox)
        self.mouse.register_button_observer(self.textbox)

        self.main_menu_button = SmallTextButton(x + 60, y + 127, 5, self.image_library, 'OK', self.go_to_main_menu)
        self.add_element(self.main_menu_button)
        self.mouse.register_button_observer(self.main_menu_button)

        self.new_game_button = SmallTextButton(x + 130 + 160, y + 127, 5, self.image_library, 'Rematch', self.start_new_game)
        self.add_element(self.new_game_button)
        self.mouse.register_button_observer(self.new_game_button)

        self.background = Image(x, y, 0, self.image_library, 'popup')
        self.add_element(self.background)


    def start_new_game(self):
        post_event(CustomEvent.CHANGE_SCREEN, screen_name=self.new_game_screen_name, color=self.player_color)

    def go_to_main_menu(self):
        post_event(CustomEvent.CHANGE_SCREEN, screen_name='main_menu')