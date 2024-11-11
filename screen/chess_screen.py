from drawing import ImageLibrary
from mouse import Mouse
from screen.screen import Screen
from chess.chess import ChessBoard, Color
from board_controller import BoardController
from view.button import Button
from view.timer import TimerBox
from view.taken_pieces_display import TakenPiecesDisplay
from custom_events import EventAnnouncer


class ChessScreen(Screen):
    def __init__(self, mouse: Mouse, image_library: ImageLibrary, event_announcer: EventAnnouncer, color: Color):
        super().__init__(mouse, image_library, event_announcer)
        game = ChessBoard(Color.WHITE)
        game.start()
        self.board_controller = BoardController(game, self.image_library, color, 80, 80)
        self.board_controller.setup(self.mouse)
        self.add_element(self.board_controller)
        
        self.rotate_button = Button(0, 0, 1, self.image_library, 'button_rotate', 'button_rotate_pressed', self.rotate)
        self.add_element(self.rotate_button)
        self.mouse.register_button_observer(self.rotate_button)
        
        self.taken_white_pieces_display = TakenPiecesDisplay(20, 20, 1, self.image_library, '', game, Color.BLACK)
        self.add_element(self.taken_white_pieces_display)
        self.event_announcer.register_observer(self.taken_white_pieces_display)

        self.taken_black_pieces_display = TakenPiecesDisplay(20, 594, 1, self.image_library, '', game, Color.WHITE)
        self.add_element(self.taken_black_pieces_display)
        self.event_announcer.register_observer(self.taken_black_pieces_display)

        self.black_timer = TimerBox(600,80,1,self.image_library, '', 120, Color.BLACK)
        self.add_element(self.black_timer)
        self.event_announcer.register_observer(self.black_timer)

        self.white_timer = TimerBox(600,564,1,self.image_library, '', 120, Color.WHITE)
        self.add_element(self.white_timer)
        self.event_announcer.register_observer(self.white_timer)

    def rotate(self):
        self.board_controller.rotate()

        white_x = self.taken_white_pieces_display.draw_x1
        white_y = self.taken_white_pieces_display.draw_y1
        black_x = self.taken_black_pieces_display.draw_x1
        black_y = self.taken_black_pieces_display.draw_y1
        self.taken_black_pieces_display.move(white_x, white_y)
        self.taken_white_pieces_display.move(black_x, black_y)

        white_x = self.white_timer.draw_x1
        white_y = self.white_timer.draw_y1
        black_x = self.black_timer.draw_x1
        black_y = self.black_timer.draw_y1
        self.black_timer.move(white_x, white_y)
        self.white_timer.move(black_x, black_y)
