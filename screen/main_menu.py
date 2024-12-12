from screen.screen import Screen
from view.view import View
from view.button import TextButton, SwitchButton
from pygame.display import get_surface
from custom_events import EventAnnouncer
from screen.chess_screen import ChessScreen
from chess.enums import Color
import pygame


class MainMenu(Screen):
    def __init__(self, mouse, image_library, event_announcer: EventAnnouncer, 
                 change_screen_function):
        super().__init__(mouse, image_library, event_announcer)
        self.change_screen = change_screen_function

        background_surface = pygame.Surface(get_surface().get_size())
        background_surface.fill('gray')
        background = View(0,0,-10,self.image_library,background_surface)
        self.add_element(background)

        self.start_game_button = TextButton(500, 300,1,self.image_library, 'Play game', self.start_chess_game)
        self.add_element(self.start_game_button)
        self.mouse.register_button_observer(self.start_game_button)

        color_button_x = self.start_game_button.draw_x1 + self.start_game_button.button_width + 30
        color_button_y = self.start_game_button.draw_y1 + (self.start_game_button.button_height - self.image_library['button_white'].get_height()) / 2
        self.color_button = SwitchButton(color_button_x, color_button_y, 1, self.image_library,
                                        ['button_white', 'button_black'],
                                        [Color.WHITE,  Color.BLACK])
        self.add_element(self.color_button)
        self.mouse.register_button_observer(self.color_button)

        self.start_practive_button = TextButton(500, 450, 1, self.image_library, 'Practice', self.start_practice_game)
        self.add_element(self.start_game_button)
        self.mouse.register_button_observer(self.start_game_button)

    def start_chess_game(self):
        chess = ChessScreen(self.mouse, self.image_library, self.event_announcer, self.color_button.get_value())
        self.change_screen(chess)
    
    def start_practice_game(self):
        chess = ChessScreen(self.mouse, self.image_library, self.event_announcer, self.color_button.get_value())
        self.change_screen(chess)
    