from game.drawing import ImageLibrary
from game.mouse import Mouse
from screen.screen import Screen
from chess.chess import Color
from game.board_controller import BoardController
from view.button import Button
from view.taken_pieces_display import TakenPiecesDisplay
from game.custom_events import EventAnnouncer, post_event, CustomEvent
from screen.game_end_popup import GameEndPopup
from view.text import Text

class PracticeChessScreen(Screen):
    def __init__(self, mouse: Mouse, image_library: ImageLibrary, event_announcer: EventAnnouncer, color: Color):
        super().__init__(mouse, image_library, event_announcer, 0, 0, '')
        self.board_controller = BoardController(self.image_library, color, 80, 80, 'mouse')
        self.board_controller.setup(self.mouse)
        self.event_announcer.register_observer(self.board_controller)
        self.add_element(self.board_controller)

        self.undo_button = Button(0, 100, 3, image_library, 'button_rewind', 'button_rewind_pressed', self.undo_last_move)
        self.add_element(self.undo_button)
        self.mouse.register_button_observer(self.undo_button)

        self.rotate_button = Button(0, 50, 1, self.image_library, 'button_rotate', 'button_rotate_pressed', self.rotate)
        self.add_element(self.rotate_button)
        self.mouse.register_button_observer(self.rotate_button)

        self.menu_button = Button(0, 0, 1, self.image_library, 'menu_button', 'menu_button_pressed', self.go_to_main_menu)
        self.add_element(self.menu_button)
        self.mouse.register_button_observer(self.menu_button)


        taken_pieces_display_x = 20
        taken_pieces_display_upper_y = 20
        taken_pieces_display_lower_y = 594

        if (color == Color.WHITE):
            taken_pieces_white_y = taken_pieces_display_lower_y
            taken_pieces_black_y = taken_pieces_display_upper_y
        else:
            taken_pieces_white_y = taken_pieces_display_upper_y
            taken_pieces_black_y = taken_pieces_display_lower_y

        self.taken_white_pieces_display = TakenPiecesDisplay(taken_pieces_display_x, taken_pieces_white_y, 1, self.image_library, '', self.board_controller.game, Color.BLACK)
        self.add_element(self.taken_white_pieces_display)
        self.event_announcer.register_observer(self.taken_white_pieces_display)

        self.taken_black_pieces_display = TakenPiecesDisplay(taken_pieces_display_x, taken_pieces_black_y, 1, self.image_library, '', self.board_controller.game, Color.WHITE)
        self.add_element(self.taken_black_pieces_display)
        self.event_announcer.register_observer(self.taken_black_pieces_display)

        for i in range(0,8):
            labels_rank = ['1','2','3','4','5','6','7','8']
            step = 64
            label_rank = Text(self.draw_x1 + 16, self.draw_y1 + 528 - step * i, 
                              self.draw_x1 + 80, self.draw_y1 + 592 - step * i,
                              1,self.image_library, labels_rank[i])
            self.add_element(label_rank)


            labels_rank = ['A','B','C','D','E','F','G','H']
            label_file = Text(self.draw_x1 + 80 + step * i, self.draw_y1 + 594, 
                              self.draw_x1 + 144 + step * i, self.draw_y1 + 658,
                              1,self.image_library, labels_rank[i])
            self.add_element(label_file)


        self.game_end_popup = None

    def rotate(self):
        self.board_controller.rotate()

        white_x = self.taken_white_pieces_display.draw_x1
        white_y = self.taken_white_pieces_display.draw_y1
        black_x = self.taken_black_pieces_display.draw_x1
        black_y = self.taken_black_pieces_display.draw_y1
        self.taken_black_pieces_display.move(white_x, white_y)
        self.taken_white_pieces_display.move(black_x, black_y)

    def update(self):
        super().update()

    def receive_event(self, event):
        if event.type == CustomEvent.FINISHED_GAME.value and self.game_end_popup == None:
            self.create_game_end_popup()    

    def create_game_end_popup(self):
        self.game_end_popup = GameEndPopup(self.mouse, self.image_library, self.event_announcer,
                                        300, 300, self.board_controller.player_color, self.board_controller.finished_game, 'practice_game')
        self.add_element(self.game_end_popup)

    def remove_game_end_popup(self):
        if self.game_end_popup == None:
            return
        self.remove_element(self.game_end_popup)
        self.game_end_popup = None

    def go_to_main_menu(self):
        post_event(CustomEvent.CHANGE_SCREEN, screen_name='main_menu')
        
    def undo_last_move(self):
        self.board_controller.undo_move()