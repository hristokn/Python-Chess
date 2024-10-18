from mouse import Clickable, LEFTMOUSEBUTTON, RIGHTMOUSEBUTTON, MOUSEBUTTONUP, MOUSEBUTTONDOWN, MOUSEMOTION, Mouse
from pygame.event import Event
from pygame import Surface
from drawing import Drawable, get_square_pos, SQUARE_SIZE, ImageLibrary, get_piece_image_name
from chess.chess import ChessBoard, Square, Color


class SquareController(Clickable, Drawable):
    def __init__(self, square, image_library: ImageLibrary,
                x1, y1, priority):
        Clickable.__init__(self, x1, y1, x1 + SQUARE_SIZE, y1 + SQUARE_SIZE, priority)
        sq_img_str = 'white_square' if square.color() == Color.WHITE else 'black_square'
        Drawable.__init__(self, x1, y1, image_library, sq_img_str)
        self.square = square
        self.move_image = 'valid_move'
        self.selected_square_image = 'selected_square' 
        self.selected = False
        self.has_move = False

    def draw(self, surface: Surface):
        Drawable.draw(self, surface)
        if self.selected:
            surface.blit(self.image_library[self.selected_square_image], (self.draw_x1,self.draw_y1))
        if self.has_move:
            surface.blit(self.image_library[self.move_image], (self.draw_x1,self.draw_y1))

    def recieve_click(self, event: Event) -> bool:
        return super().recieve_click(event)

    def recieve_mouse_motion(self, event: Event):
        pass

class PieceController(Clickable, Drawable):
    def __init__(self, piece, image_library: ImageLibrary,
                x1, y1, priority):
        image = get_piece_image_name(piece.color, piece.type)
        Clickable.__init__(self, x1, y1, x1 + SQUARE_SIZE, y1 + SQUARE_SIZE, priority)
        Drawable.__init__(self, x1, y1, image_library, image)
        self.piece = piece
        self.take_image = 'valid_take'
        self.is_held = False
        self.can_be_taken = False

    def recieve_click(self, event: Event) -> bool:
        return super().recieve_click(event)

    def recieve_mouse_motion(self, event: Event):
        x,y = event.pos
        if self.is_held:
            self.draw_x1 = x - SQUARE_SIZE/2
            self.draw_y1 = y - SQUARE_SIZE/2

    def draw(self, surface: Surface):
        Drawable.draw(self, surface)
        if self.can_be_taken:
            surface.blit(self.image_library[self.take_image], (self.draw_x1,self.draw_y1))

    def set_held_piece(self):
        self.is_held = True
        self.priority = self.priority + 1

    def clear_held_piece(self):
        self.is_held = False
        self.draw_x1 = self.x1
        self.draw_y1 = self.y1
        self.priority = self.priority - 1
        
    def update_image(self):
        self.image = get_piece_image_name(self.piece.color, self.piece.type)

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

class BoardController(Drawable):
    def __init__(self, chess_game: ChessBoard, image_library: ImageLibrary, color,
                 board_x, board_y):
        board_draw = Surface((8*SQUARE_SIZE, 8*SQUARE_SIZE))
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
        self.priority = 0

    def setup(self, mouse: Mouse):
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

    def update(self):
        self.handle_clicked_pieces()

    def update_pieces(self):
        for p in self.piece_controllers:
            square = self.game.find_square(p.piece)
            if square == Square.UNKNOWN:
                self.piece_controllers.remove(p)
            x, y = get_square_pos(self.board_x, self.board_y, square, self.color)
            p.draw_x1 = x
            p.draw_y1 = y
            p.x1 = x
            p.y1 = y
            p.x2 = x + SQUARE_SIZE
            p.y2 = y + SQUARE_SIZE
            p.update_image()
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

    def try_move(self, target):
        if isinstance(target, PieceController):
            target = target.piece
            square = self.game.find_square(target)
        else:
            square = target.square
        if self.game.play_move(self.selected_piece.piece, square):
            self.update_pieces()
        