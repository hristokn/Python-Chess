from screen.screen import Screen
from game.custom_events import post_event, CustomEvent
from view.view import View
from view.button import TextButton, SwitchButton
from pygame.display import get_surface
from game.custom_events import EventAnnouncer
from screen.chess_screen import ChessScreen
from chess.enums import Color
from game.sound_player import SoundPlayer
import pygame


class MainMenu(Screen):
    def __init__(
        self,
        mouse,
        image_library,
        event_announcer: EventAnnouncer,
        sound_player: SoundPlayer,
    ):
        super().__init__(mouse, image_library, event_announcer, sound_player, 0, 0, "")

        background_surface = pygame.Surface(get_surface().get_size())
        background_surface.fill("gray")
        background = View(0, 0, -10, self.image_library, background_surface)
        self.add_element(background)

        self.start_game_button = TextButton(
            500, 300, 1, self.image_library, "Play game", self.start_chess_game
        )
        self.add_element(self.start_game_button)
        self.mouse.register_button_observer(self.start_game_button)

        self.start_practice_button = TextButton(
            500, 400, 1, self.image_library, "Practice", self.start_practice_game
        )
        self.add_element(self.start_practice_button)
        self.mouse.register_button_observer(self.start_practice_button)

        color_button_x = (
            self.start_game_button.draw_x1 + self.start_game_button.width() + 30
        )
        color_button_y = (
            self.start_game_button.draw_y1
            + (
                self.start_game_button.height()
                - self.image_library["button_white"].get_height()
            )
            / 2
        )
        self.color_button = SwitchButton(
            color_button_x,
            color_button_y,
            1,
            self.image_library,
            ["button_white", "button_black"],
            [Color.WHITE, Color.BLACK],
        )
        self.add_element(self.color_button)
        self.mouse.register_button_observer(self.color_button)

        self.start_practive_button = TextButton(
            500, 450, 1, self.image_library, "Practice", self.start_practice_game
        )
        self.add_element(self.start_game_button)
        self.mouse.register_button_observer(self.start_game_button)

    def start_chess_game(self):
        post_event(
            CustomEvent.CHANGE_SCREEN,
            screen_name="chess_game",
            color=self.color_button.get_value(),
        )

    def start_practice_game(self):
        post_event(
            CustomEvent.CHANGE_SCREEN,
            screen_name="practice_game",
            color=self.color_button.get_value(),
        )
