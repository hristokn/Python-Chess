from screen.screen import Screen
from game.drawing import ImageLibrary
from game.mouse import Mouse
from game.custom_events import EventAnnouncer, post_event, CustomEvent
from game.sound_player import SoundPlayer
from game.chess_sounds import ChessBoardSoundPlayer
from view.button import Button
from view.taken_pieces_display import TakenPiecesDisplay
from view.text import Text
from chess.enums import Color
from abc import ABC, abstractmethod


class BaseChessScreen(Screen, ABC):
    def __init__(
        self,
        mouse: Mouse,
        image_library: ImageLibrary,
        event_announcer: EventAnnouncer,
        sound_player: SoundPlayer,
        color: Color,
        board_controller,
    ):
        super().__init__(mouse, image_library, event_announcer, sound_player, 0, 0, "")
        self.board_controller = board_controller
        self.board_controller.setup(self.mouse)
        self.event_announcer.register_observer(self.board_controller)
        self.add_element(self.board_controller)

        self.rotate_button = Button(
            0,
            50,
            1,
            self.image_library,
            "button_rotate",
            "button_rotate_pressed",
            self.rotate,
        )
        self.add_element(self.rotate_button)
        self.mouse.register_button_observer(self.rotate_button)

        self.menu_button = Button(
            0,
            0,
            1,
            self.image_library,
            "menu_button",
            "menu_button_pressed",
            self.go_to_main_menu,
        )
        self.add_element(self.menu_button)
        self.mouse.register_button_observer(self.menu_button)

        taken_pieces_display_x = 20
        taken_pieces_display_upper_y = 20
        taken_pieces_display_lower_y = 594

        if color == Color.WHITE:
            taken_pieces_white_y = taken_pieces_display_lower_y
            taken_pieces_black_y = taken_pieces_display_upper_y
        else:
            taken_pieces_white_y = taken_pieces_display_upper_y
            taken_pieces_black_y = taken_pieces_display_lower_y

        self.taken_white_pieces_display = TakenPiecesDisplay(
            taken_pieces_display_x,
            taken_pieces_white_y,
            1,
            self.image_library,
            "",
            self.board_controller.game,
            Color.BLACK,
        )
        self.add_element(self.taken_white_pieces_display)
        self.event_announcer.register_observer(self.taken_white_pieces_display)

        self.taken_black_pieces_display = TakenPiecesDisplay(
            taken_pieces_display_x,
            taken_pieces_black_y,
            1,
            self.image_library,
            "",
            self.board_controller.game,
            Color.WHITE,
        )
        self.add_element(self.taken_black_pieces_display)
        self.event_announcer.register_observer(self.taken_black_pieces_display)

        for i in range(8):
            labels_rank = ["1", "2", "3", "4", "5", "6", "7", "8"]
            step = 64
            label_rank = Text(
                self.draw_x1 + 16,
                self.draw_y1 + 528 - step * i,
                self.draw_x1 + 80,
                self.draw_y1 + 592 - step * i,
                1,
                self.image_library,
                labels_rank[i],
            )
            self.add_element(label_rank)

            labels_file = ["A", "B", "C", "D", "E", "F", "G", "H"]
            label_file = Text(
                self.draw_x1 + 80 + step * i,
                self.draw_y1 + 594,
                self.draw_x1 + 144 + step * i,
                self.draw_y1 + 658,
                1,
                self.image_library,
                labels_file[i],
            )
            self.add_element(label_file)

        self.game_end_popup = None

        chess_board_sound_player = ChessBoardSoundPlayer(self.sound_player)
        self.add_element(chess_board_sound_player)
        self.event_announcer.register_observer(chess_board_sound_player)

    def rotate(self):
        self.board_controller.rotate()

        white_x = self.taken_white_pieces_display.draw_x1
        white_y = self.taken_white_pieces_display.draw_y1
        black_x = self.taken_black_pieces_display.draw_x1
        black_y = self.taken_black_pieces_display.draw_y1
        self.taken_black_pieces_display.move(white_x, white_y)
        self.taken_white_pieces_display.move(black_x, black_y)

    def receive_event(self, event):
        if (
            event.type == CustomEvent.FINISHED_GAME.value
            and self.game_end_popup is None
        ):
            self.create_game_end_popup()

    @abstractmethod
    def create_game_end_popup(self): ...

    def go_to_main_menu(self):
        post_event(CustomEvent.CHANGE_SCREEN, screen_name="main_menu")
