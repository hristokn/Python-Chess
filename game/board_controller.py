from game.mouse import Mouse
from pygame.event import Event
from game.custom_events import CustomEvent, post_event, EventObserver
from pygame import Surface
from game.drawing import Drawable, get_square_pos, SQUARE_SIZE, ImageLibrary
from chess.chess import ChessBoard, Square, Color, Piece
from chess.finished_game import FinishedGame, VictoryType
from view.view import View
from view.chess_controller import SquareController, PieceController
from view.promotion_picker import PromotionPicker
from game.chess_input import ChessInput,MouseChessInput, AIChessInput

def get_square_controller(square_controllers: list[SquareController], sq: Square):
    sc = None
    for _sc in square_controllers:
        if _sc.square == sq:
            sc = _sc
            break
    return sc

def get_piece_controller(piece_controllers: list[PieceController], piece):
    piece_controller = None
    for _piece in piece_controllers:
        if _piece.piece == piece:
            piece_controller = _piece
            break
    return piece_controller

class BoardController(View):
    def __init__(self, image_library: ImageLibrary,
                 color, x, y, opponent_input: str):
        board_background = Surface((8 * SQUARE_SIZE, 8 * SQUARE_SIZE))
        View.__init__(self, x, y, 10, image_library, board_background)
        self.game = ChessBoard(Color.WHITE)
        self.game.start()
        self.color_pov = color
        self.player_color = color
        self.x = x
        self.y = y

        self._promotion_picker: PromotionPicker = None
        self._promotion_target = None
        self._promotion_piece = None
        self.piece_controllers: list[PieceController] = []
        self.square_controllers: list[SquareController] = []
        self.selected_piece = None
        self.held_piece = None
        self.game_ended = False
        
        opponent_color = self.player_color.next()
        player_input = MouseChessInput(self)
        if opponent_input == 'ai':
            input = AIChessInput(self, opponent_color)
        elif opponent_input == 'mouse':
            input = player_input
        else:
            raise ValueError

        self.chess_inputs:dict[Color, ChessInput] = {self.player_color: player_input, opponent_color: input}

    def setup(self, mouse: Mouse):
        self.mouse = mouse
        mouse.register_button_observer(self)
        for square, piece in self.game.board.items():
            x,y = get_square_pos(self.x, self.y, square, self.color_pov)
            self.add_square(square, x, y)
            if piece != None:
                self.add_piece(piece, x, y)

    def add_square(self, square: Square, x, y):
        sc = SquareController(square, self.image_library, x, y, 1)
        self.square_controllers.append(sc)
        self.mouse.register_button_observer(sc)

    def add_piece(self, piece: Piece, x, y):
        pc = PieceController(piece, self.image_library, x, y, 2)
        self.piece_controllers.append(pc)
        self.mouse.register_button_observer(pc) 
        self.mouse.register_motion_observer(pc)

    def rotate(self):
        self.color_pov = self.color_pov.next()
        for sc in self.square_controllers:
            square = sc.square
            x,y = get_square_pos(self.x, self.y, square, self.color_pov)
            sc.move(x,y)
        
        if self._promotion_picker != None:
            self._promotion_picker.rotate()    

        self.update_pieces()    

    def draw(self, surface):
        Drawable.draw(self, surface)
        for sq in self.square_controllers:
            sq.draw(surface)
      
        for p in self.piece_controllers:
            p.draw(surface)
        try:    
            self.held_piece.draw(surface)
        except AttributeError:
            pass
       
        if self._promotion_picker != None:
            self._promotion_picker.draw(surface)

    def update(self):
        if self._promotion_picker != None:
            self._promotion_picker.update()
        if self.game_ended:
            return
        for input in self.chess_inputs.values():
            input.update()
        move = self.chess_inputs[self.game.color_to_play].get_move()
        self.try_move(move)

    def update_pieces(self):
        for square, piece in self.game.board.items():
            if piece != None and not any(pc.piece == piece for pc in self.piece_controllers):
                x,y = get_square_pos(self.x, self.y, square, self.color_pov)
                self.add_piece(piece, x, y)

        for removed_piece in filter(lambda pc: self.game.find_square(pc.piece) == Square.UNKNOWN, self.piece_controllers):
            self.mouse.unregister_button_observer(removed_piece)
            self.mouse.unregister_motion_observer(removed_piece)

        self.piece_controllers = list(filter(lambda pc: self.game.find_square(pc.piece) != Square.UNKNOWN,
                                              self.piece_controllers))
        for p in self.piece_controllers:
            square = self.game.find_square(p.piece)
            x, y = get_square_pos(self.x, self.y, square, self.color_pov)
            p.move(x,y)
            p.update_image()
    
    def highlight_last_move(self):
        if len(self.game.past_moves) == 0:
            return
        move = self.game.past_moves[-1]
        for sq in move.changes.keys():
            self.highlight_square(sq)

    def unhighlight_last_move(self):
        if len(self.game.past_moves) == 0:
            return
        move = self.game.past_moves[-1]
        for sq in move.changes.keys():
            self.unhighlight_square(sq)

    def highlight_square(self, square: Square):
        sc = get_square_controller(self.square_controllers, square)
        sc.selected = True

    def unhighlight_square(self, square: Square):
        sc = get_square_controller(self.square_controllers, square)
        sc.selected = False

    def select_piece(self, piece: PieceController):
        self.selected_piece = piece
        self.highlight_square(self.game.find_square(piece.piece))
        for move in filter(lambda move: move.piece == piece.piece, self.game.possible_moves):
            end_square = move.get_end_square()
            end_piece = self.game.board[end_square] 
            if end_piece == None:
                sc = get_square_controller(self.square_controllers, end_square)
                sc.has_move = True
            else:
                pc = get_piece_controller(self.piece_controllers, end_piece)
                pc.can_be_taken = True

    def deselect_piece(self):
        if self.selected_piece != None:
            self.unhighlight_square(self.game.find_square(self.selected_piece.piece))
            for sc in self.square_controllers:
                sc.has_move = False
            for pc in self.piece_controllers:
                pc.can_be_taken = False
            self.selected_piece = None

    def set_held_piece(self, piece: PieceController):
        self.held_piece = piece
        piece.set_held_piece()
        self.update_pieces()

    def clear_held_piece(self):
        if self.held_piece != None:
            self.held_piece.clear_held_piece()
            self.held_piece = None
            self.update_pieces()

    def create_promotion_picker(self, piece, square):
        x, y = get_square_pos(self.x, self.y, square, self.color_pov)
        draw_down = (self.color_pov == self.game.color_to_play)
        if not draw_down:
            y -= SQUARE_SIZE*3

        self._promotion_picker = PromotionPicker(self.x, self.y, x, y, 5, self.image_library, self.game.color_to_play, draw_down, self.pick_promotion)
        for button in self._promotion_picker._buttons:
            self.mouse.register_button_observer(button)
        self.mouse.register_button_observer(self._promotion_picker)

        pc = get_piece_controller(self.piece_controllers, piece)
        pc.hide()
        self._promotion_piece = piece
        self._promotion_target = square

    def remove_promotion_picker(self):
        for button in self._promotion_picker._buttons:
            self.mouse.unregister_button_observer(button)
        self.mouse.unregister_button_observer(self._promotion_picker)
        self._promotion_picker = None
        self._promotion_piece = None
        self._promotion_target = None

    def pick_promotion(self, piece_type):
        move = self.game.get_promotion_move(self._promotion_piece, self._promotion_target, piece_type)
        if not self.try_move(move):
            raise RuntimeError
        
        x,y = get_square_pos(self.x, self.y, self._promotion_target, self.color_pov)
        self.add_piece(self.game.board[self._promotion_target], x, y)

        self.remove_promotion_picker()

    def post_played_move_event(self, move, color: Color):
        if self.game.in_checkmate():
            post_event(CustomEvent.PLAYED_MOVE, color=color, is_checkmate=True)
        elif self.game.king_in_check(color.next()):
            post_event(CustomEvent.PLAYED_MOVE, color=color, is_check=True)
        elif getattr(move, 'is_castle', False):
            post_event(CustomEvent.PLAYED_MOVE, color=color, is_castle=True)
        elif self._promotion_picker != None:
            post_event(CustomEvent.PLAYED_MOVE, color=color, is_promotion=True)
        elif len(move.taken) != 0:
            post_event(CustomEvent.PLAYED_MOVE, color=color, is_capture=True)
        else:
            post_event(CustomEvent.PLAYED_MOVE, color=color)

    def try_move(self, move) -> bool:
        _color=self.game.color_to_play
        self.unhighlight_last_move()
        played = self.game.play_move(move)
        if played:
            self.update_pieces()
            self.post_played_move_event(move, _color)
            self.try_finish_game()
        self.highlight_last_move()
        return played

    def recieve_click(self, event: Event) -> bool:
        x,y = event.pos
        if not self.collides(x,y):
            self.outside_click()
        elif self.collides(x,y) and self._promotion_picker != None and not self._promotion_picker.collides(x,y):
            return True
        return False

    def outside_click(self):
        if self.held_piece != None:
            self.clear_held_piece()
        if self.selected_piece != None: 
            self.deselect_piece()
    
    def receive_event(self, event):
        if event.type == CustomEvent.TIMER_END.value:
            self.finish_game(VictoryType.TIMEOUT, event.color.next())

    def try_finish_game(self):
        if self.game_ended:
            pass
        elif self.game.in_draw():
            self.finish_game(VictoryType.DRAW, None)
        elif self.game.in_checkmate():
            self.finish_game(VictoryType.CHECKMATE, self.game.color_to_play.previous())

    def finish_game(self, victory_type: VictoryType, color: Color):
            self.game_ended = True
            self.finished_game = FinishedGame(self.game, color, victory_type)
            post_event(CustomEvent.FINISHED_GAME, color = color)

    def undo_move(self):
        self.game.undo_last_move()
        self.update_pieces()
        post_event(CustomEvent.UNDID_MOVE)

    def destroy(self):
        for pc in self.piece_controllers:
            self.mouse.unregister_button_observer(pc)
            self.mouse.unregister_motion_observer(pc)
        for sq in self.square_controllers:
            self.mouse.unregister_button_observer(sq)
        self.mouse.unregister_button_observer(self._promotion_picker)
        return super().destroy()