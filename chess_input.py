from chess.moves import Move
from chess.ai import AIMove
from view.chess_controller import PieceController, SquareController
from abc import ABC, abstractmethod

class ChessInput(ABC):
    def __init__(self, board_controller) -> None:
        self.waiting_for_move = False
        self.board_controller = board_controller

    @abstractmethod
    def get_move(self) -> Move | None:
        pass

    def update(self):
        pass

class MouseChessInput(ChessInput):
    def __init__(self, board_controller) -> None:
        super().__init__(board_controller)
        self.move = None
        self.has_premove = False
        self.premove_piece = None
        self.premove_square = None

    def get_move(self) -> Move | None:
        if self.has_premove:
            self.waiting_for_move = False
            return self.use_premove()
        elif self.move == None:
            self.waiting_for_move = True
            return None
        else:
            self.waiting_for_move = False
            _move = self.move
            self.move = None
            return _move

    def update(self):
        self.handle_clicked_pieces()

    def handle_clicked_pieces(self):
        down = None
        up = None
        for piece in self.board_controller.piece_controllers:
            if piece.left_buttop_down:
                down = piece
            if piece.left_buttop_up:
                up = piece

        for square in self.board_controller.square_controllers:
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
        if self.board_controller.selected_piece == None:
            self.board_controller.select_piece(piece)
            self.board_controller.set_held_piece(piece)
        elif self.board_controller.selected_piece == piece:
            self.board_controller.set_held_piece(piece)
        else:
            self.create_move_piece(piece)

    def squaredown(self, square):
        if self.board_controller.selected_piece != None:
            self.create_move_square(square.square)

    def up(self, obj):
        if isinstance(obj, PieceController):
            self.pieceup(obj)
        if isinstance(obj, SquareController):
            self.squareup(obj)

    def pieceup(self, piece):
        if self.board_controller.selected_piece == piece:
            self.board_controller.clear_held_piece()
        elif self.board_controller.selected_piece != None and self.board_controller.held_piece != None:
            self.create_move_piece(piece)
            self.board_controller.clear_held_piece()

    def squareup(self, square):
        if self.board_controller.selected_piece == None:
            pass
        elif self.board_controller.held_piece == None:
            self.board_controller.deselect_piece()
        elif self.board_controller.held_piece != None:
            self.create_move_square(square.square)
            self.board_controller.clear_held_piece()

    def create_move_piece(self, target):
        square = self.board_controller.game.find_square(target.piece)
        self.create_move_square(square)

    def create_move_square(self, square):
        selected_piece = self.board_controller.selected_piece.piece
        self.board_controller.deselect_piece()
        
        if self.has_premove:
            self.remove_premove()

        if self.board_controller.game.multiple_moves_exist(selected_piece, square):
            self.board_controller.create_promotion_picker(selected_piece, square)
        elif self.waiting_for_move:
            self.move = self.board_controller.game.find_move(selected_piece, square)
        else:
            self.save_premove(selected_piece, square)

    def save_premove(self, piece, square):
        self.has_premove = True
        self.premove_piece = piece
        self.board_controller.highlight_square(self.board_controller.game.find_square(piece))
        self.premove_square = square
        self.board_controller.highlight_square(square)

    def remove_premove(self):
        self.board_controller.unhighlight_square(self.board_controller.game.find_square(self.premove_piece))
        self.board_controller.unhighlight_square(self.premove_square)
        self.has_premove = False
        self.premove_piece = None
        self.premove_square = None
    
    def use_premove(self) -> Move:
        # if self.board_controller.get_piece_controller(self.premove_piece) == None:
        #     self.has_premove = False
        #     self.premove_piece = None
        #     self.premove_square = None
        #     return None
        _premove_piece = self.premove_piece 
        _premove_square = self.premove_square
        self.remove_premove()
        return self.board_controller.game.find_move(_premove_piece, _premove_square)


class AIChessInput(ChessInput):
    thread = None
    move = None
    def get_move(self) -> Move | None:
        if self.move == None and self.thread == None:
            self.thread = AIMove(self.board_controller.game)
            self.thread.start()
            self.waiting_for_move = True
            return None
        elif self.move != None:
            _move = self.move
            self.move = None
            return _move
        else:
            return None

    def update(self):
        if self.waiting_for_move and not self.thread.is_alive():
            self.move = self.thread.move
            self.thread = None
            self.waiting_for_move = False
        else:
            pass

class NetworkChessInput(ChessInput):
    pass