from mouse import Clickable, Mouse
from pygame.event import Event
from custom_events import CustomEvent, post_event
from pygame import Surface
from drawing import Drawable, get_square_pos, SQUARE_SIZE, ImageLibrary
from chess.chess import ChessBoard, Square
from chess_controller import SquareController, PieceController
from promotion_picker import PromotionPicker

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

class BoardController(Drawable, Clickable):
    def __init__(self, chess_game: ChessBoard, image_library: ImageLibrary, color,
                 board_x, board_y):
        width = 8 * SQUARE_SIZE
        Clickable.__init__(self, board_x, board_y, board_x + width, board_y + width, 10)
        board_draw = Surface((width, width))
        board_draw.fill((255,255,255))
        Drawable.__init__(self, board_x, board_x, image_library, board_draw)
        self.game = chess_game
        self.piece_controllers: list[PieceController] = []
        self.square_controllers: list[SquareController] = []
        self.selected_piece = None
        self.held_piece = None
        self.color = color
        self.board_x = board_x
        self.board_y = board_y
        self._promotion_picker: PromotionPicker = None
        self._promotion_target = None
        self._promotion_piece = None

    def setup(self, mouse: Mouse):
        self.mouse = mouse
        mouse.register_button_observer(self)
        for square, piece in self.game.board.items():
            pos = get_square_pos(self.board_x, self.board_y, square, self.color)
            sc = SquareController(square, self.image_library, pos[0], pos[1], 1)
            self.square_controllers.append(sc)
            mouse.register_button_observer(sc)
            if piece != None:
                pc = PieceController(piece, self.image_library, pos[0], pos[1], 2)
                self.piece_controllers.append(pc)
                mouse.register_button_observer(pc) 
                mouse.register_motion_observer(pc)

    def draw(self, surface):
        Drawable.draw(self, surface)
        for sq in self.square_controllers:
            sq.draw(surface)
        for p in self.piece_controllers:
            p.draw(surface)
        if self._promotion_picker != None:
            self._promotion_picker.draw(surface)

    def update(self):
        self.handle_clicked_pieces()
        if self._promotion_picker != None:
            self._promotion_picker.update()

    def update_pieces(self):
        removed = []
        for p in self.piece_controllers:
            square = self.game.find_square(p.piece)
            if square == Square.UNKNOWN:
                removed.append(p)
                continue
            x, y = get_square_pos(self.board_x, self.board_y, square, self.color)
            p.draw_x1 = x
            p.draw_y1 = y
            p.x1 = x
            p.y1 = y
            p.x2 = x + SQUARE_SIZE
            p.y2 = y + SQUARE_SIZE
            p.update_image()
        for p in removed:
            self.piece_controllers.remove(p)
            self.mouse.unregister_button_observer(p)
            self.mouse.unregister_motion_observer(p)
        self.piece_controllers.sort(key=lambda p: p.priority)
    
    def select_piece(self, piece: PieceController):
        self.selected_piece = piece
        square = self.game.find_square(piece.piece)
        sc = get_square_controller(self.square_controllers, square)
        sc.selected = True
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
        for sc in self.square_controllers:
            sc.selected = False
            sc.has_move = False
        for pc in self.piece_controllers:
            pc.can_be_taken = False
        self.selected_piece = None

    def set_held_piece(self, piece: PieceController):
        self.held_piece = piece
        piece.set_held_piece()
        self.update_pieces()

    def clear_held_piece(self):
        self.held_piece.clear_held_piece()
        self.held_piece = None
        self.update_pieces()

    def handle_clicked_pieces(self):
        down = None
        up = None
        for piece in self.piece_controllers:
            if piece.left_buttop_down:
                down = piece
            if piece.left_buttop_up:
                up = piece

        for square in self.square_controllers:
            if square.left_buttop_down:
                down = square
            if square.left_buttop_up:
                up = square

        if down != None:
            self.down(down)
            down.left_buttop_down = False
        if up != None:
            self.up(up)
            up.left_buttop_up = False

    def down(self, obj):
        if isinstance(obj, PieceController):
            self.piecedown(obj)
        if isinstance(obj, SquareController):
            self.squaredown(obj)
        
    def piecedown(self, piece):
        if self.selected_piece == None:
            self.select_piece(piece)
            self.set_held_piece(piece)
        elif self.selected_piece == piece:
            self.set_held_piece(piece)
        else:
            self.try_move(piece)
            self.deselect_piece()

    def squaredown(self, square):
        if self.selected_piece != None:
            self.try_move(square)
            self.deselect_piece()

    def up(self, obj):
        if isinstance(obj, PieceController):
            self.pieceup(obj)
        if isinstance(obj, SquareController):
            self.squareup(obj)

    def outside_click(self):
        if self.held_piece != None:
            self.clear_held_piece()
        if self.selected_piece != None:
            self.deselect_piece()

    def pieceup(self, piece):
        if self.selected_piece == piece:
            self.clear_held_piece()
        elif self.selected_piece != None and self.held_piece != None:
            self.try_move(piece)
            self.deselect_piece()
            self.clear_held_piece()

    def squareup(self, square):
        if self.selected_piece == None:
            pass
        elif self.held_piece == None:
            self.deselect_piece()
        elif self.held_piece != None:
            self.try_move(square)
            self.deselect_piece()
            self.clear_held_piece()

    def create_promotion_picker(self, piece, square):
        x, y = get_square_pos(self.board_x, self.board_y, square, self.color)
        draw_down = (self.color == self.game.color_to_play)
        if not draw_down:
            y -= SQUARE_SIZE*3

        self._promotion_picker = PromotionPicker(x, y, 5, self.image_library, self.game.color_to_play, draw_down, self.pick_promotion)
        for button in self._promotion_picker._buttons:
            self.mouse.register_button_observer(button)
        self.mouse.register_button_observer(self._promotion_picker)

        pc = get_piece_controller(self.piece_controllers, piece)
        self.piece_controllers.remove(pc)
        self.mouse.unregister_button_observer(pc)
        self.mouse.unregister_motion_observer(pc)
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
        _color=self.game.color_to_play
        if not self.game.play_move(self.game.get_promotion_move(self._promotion_piece, self._promotion_target, piece_type)):
            raise RuntimeError
        
        x,y = get_square_pos(self.board_x, self.board_y, self._promotion_target, self.color)
        pc = PieceController(self.game.board[self._promotion_target], self.image_library, x, y, 2)
        self.piece_controllers.append(pc)
        self.mouse.register_button_observer(pc) 
        self.mouse.register_motion_observer(pc)

        self.remove_promotion_picker()
        self.update_pieces()
        post_event(CustomEvent.PLAYED_MOVE, color=_color)

    def try_move(self, target):
        if isinstance(target, PieceController):
            target = target.piece
            square = self.game.find_square(target)
        else:
            square = target.square

        _color=self.game.color_to_play
        if self.game.multiple_moves_exist(self.selected_piece.piece, square):
            self.create_promotion_picker(self.selected_piece.piece, square)
        elif self.game.play_move(self.game.find_move(self.selected_piece.piece, square)):
            self.update_pieces()
            post_event(CustomEvent.PLAYED_MOVE, color=_color)

    def recieve_click(self, event: Event) -> bool:
        x,y = event.pos
        if not self.collides(x,y):
            self.outside_click()
        elif self.collides(x,y) and self._promotion_picker != None and not self._promotion_picker.collides(x,y):
            return True
        return False

    def recieve_mouse_motion(self, event: Event):
        return super().recieve_mouse_motion(event)
    