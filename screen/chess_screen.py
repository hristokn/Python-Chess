from drawing import ImageLibrary
from mouse import Mouse
from screen.screen import Screen
from chess.chess import ChessBoard, Color
from board_controller import BoardController
from view.button import Button
from view.timer import TimerBox
from view.taken_pieces_display import TakenPiecesDisplay
from custom_events import EventAnnouncer, post_event, CustomEvent
from screen.game_end_popup import GameEndPopup


class ChessScreen(Screen):
    def __init__(self, mouse: Mouse, image_library: ImageLibrary, event_announcer: EventAnnouncer, color: Color):
        super().__init__(mouse, image_library, event_announcer, 0, 0, '')
        self.board_controller = BoardController(self.image_library, color, 80, 80)
        self.board_controller.setup(self.mouse)
        self.event_announcer.register_observer(self.board_controller)
        self.add_element(self.board_controller)
        self.game = self.board_controller.game
        
        self.rotate_button = Button(0, 0, 1, self.image_library, 'button_rotate', 'button_rotate_pressed', self.rotate)
        self.add_element(self.rotate_button)
        self.mouse.register_button_observer(self.rotate_button)
        

        taken_pieces_display_x = 20
        taken_pieces_display_upper_y = 20
        taken_pieces_display_lower_y = 594
        timer_x = 600
        timer_upper_y = 80
        timer_lower_y = 564

        if (color == Color.WHITE):
            taken_pieces_white_y = taken_pieces_display_lower_y
            taken_pieces_black_y = taken_pieces_display_upper_y
            timer_white_y = timer_lower_y
            timer_black_y = timer_upper_y
        else:
            taken_pieces_white_y = taken_pieces_display_upper_y
            taken_pieces_black_y = taken_pieces_display_lower_y
            timer_white_y = timer_upper_y
            timer_black_y = timer_lower_y


        self.taken_white_pieces_display = TakenPiecesDisplay(taken_pieces_display_x, taken_pieces_white_y, 1, self.image_library, '', self.game, Color.BLACK)
        self.add_element(self.taken_white_pieces_display)
        self.event_announcer.register_observer(self.taken_white_pieces_display)

        self.taken_black_pieces_display = TakenPiecesDisplay(taken_pieces_display_x, taken_pieces_black_y, 1, self.image_library, '', self.game, Color.WHITE)
        self.add_element(self.taken_black_pieces_display)
        self.event_announcer.register_observer(self.taken_black_pieces_display)

        self.black_timer = TimerBox(timer_x, timer_black_y, 1, self.image_library, '', 120, Color.BLACK)
        self.add_element(self.black_timer)
        self.event_announcer.register_observer(self.black_timer)

        self.white_timer = TimerBox(timer_x, timer_white_y, 1, self.image_library, '', 3, Color.WHITE)
        self.add_element(self.white_timer)
        self.event_announcer.register_observer(self.white_timer)

        self.game_end_popup = None

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
    
    def update(self):
        super().update()
        if self.board_controller.game_ended and self.game_end_popup == None:
            self.create_game_end_popup()    

    def create_game_end_popup(self):
        self.game_end_popup = GameEndPopup(self.mouse, self.image_library, self.event_announcer,
                                           300, 300, self.board_controller.color, self.board_controller.finished_game)
        self.add_element(self.game_end_popup)

    def remove_game_end_popup(self):
        if self.game_end_popup == None:
            return
        self.remove_element(self.game_end_popup)
        self.game_end_popup = None

    def go_to_main_menu(self):
        post_event(CustomEvent.CHANGE_SCREEN, screen_name='main_menu')
        
