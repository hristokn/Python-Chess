from screen.base_chess_screen import BaseChessScreen
from game.board_controller import BoardController
from view.button import Button
from chess.enums import Color
from screen.game_end_popup import GameEndPopup


class PracticeChessScreen(BaseChessScreen):
    def __init__(self, mouse, image_library, event_announcer, sound_player, color):
        board_controller = BoardController(image_library, color, 80, 80, 'mouse')
        super().__init__(mouse, image_library, event_announcer, sound_player, color, board_controller)

        self.undo_button = Button(0, 100, 3, image_library, 'button_rewind', 'button_rewind_pressed', self.undo_last_move)
        self.add_element(self.undo_button)
        self.mouse.register_button_observer(self.undo_button)

    def create_game_end_popup(self):
        self.game_end_popup = GameEndPopup(self.mouse, self.image_library, self.event_announcer, self.sound_player,
                                           300, 300, self.board_controller.player_color, self.board_controller.finished_game, 'practice_game')
        self.add_element(self.game_end_popup)

    def undo_last_move(self):
        self.board_controller.undo_move()