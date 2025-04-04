from screen.base_chess_screen import BaseChessScreen
from game.board_controller import BoardController
from view.timer import TimerBox
from chess.enums import Color
from screen.game_end_popup import GameEndPopup


class ChessScreen(BaseChessScreen):
    def __init__(self, mouse, image_library, event_announcer, sound_player, color):
        board_controller = BoardController(image_library, color, 80, 80, "ai")
        super().__init__(
            mouse, image_library, event_announcer, sound_player, color, board_controller
        )

        timer_x = 600
        timer_upper_y = 80
        timer_lower_y = 564

        if color == Color.WHITE:
            timer_white_y = timer_lower_y
            timer_black_y = timer_upper_y
        else:
            timer_white_y = timer_upper_y
            timer_black_y = timer_lower_y

        self.black_timer = TimerBox(
            timer_x, timer_black_y, 1, self.image_library, "", 999, Color.BLACK
        )
        self.add_element(self.black_timer)
        self.event_announcer.register_observer(self.black_timer)

        self.white_timer = TimerBox(
            timer_x, timer_white_y, 1, self.image_library, "", 999, Color.WHITE
        )
        self.add_element(self.white_timer)
        self.event_announcer.register_observer(self.white_timer)

    def rotate(self):
        super().rotate()
        white_x = self.white_timer.draw_x1
        white_y = self.white_timer.draw_y1
        black_x = self.black_timer.draw_x1
        black_y = self.black_timer.draw_y1
        self.black_timer.move(white_x, white_y)
        self.white_timer.move(black_x, black_y)

    def create_game_end_popup(self):
        self.game_end_popup = GameEndPopup(
            self.mouse,
            self.image_library,
            self.event_announcer,
            self.sound_player,
            300,
            300,
            self.board_controller.player_color,
            self.board_controller.finished_game,
            "chess_game",
        )
        self.add_element(self.game_end_popup)
