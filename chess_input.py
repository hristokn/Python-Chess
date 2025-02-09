from chess.moves import Move
from chess.ai import pick_move
from view.chess_controller import PieceController, SquareController
from abc import ABC, abstractmethod
from custom_events import CustomEvent, post_event

class ChessInput(ABC):
    waiting_for_move = False
    def __init__(self, board_controller) -> None:
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

    def get_move(self) -> Move | None:
        if self.move == None:
            self.waiting_for_move = True
            return None
        else:
            return self.send_move()

    def update(self):
        self.handle_clicked_pieces()
        # if self.waiting_for_move and self.move != None:
        #     self.send_move()
            
    def send_move(self):
        self.waiting_for_move = False
        _move = self.move
        self.move = None
        return _move

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
            self.board_controller.deselect_piece()

    def squaredown(self, square):
        if self.board_controller.selected_piece != None:
            self.create_move_square(square.square)
            self.board_controller.deselect_piece()

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
            self.board_controller.deselect_piece()
            self.board_controller.clear_held_piece()

    def squareup(self, square):
        if self.board_controller.selected_piece == None:
            pass
        elif self.board_controller.held_piece == None:
            self.board_controller.deselect_piece()
        elif self.board_controller.held_piece != None:
            self.create_move_square(square.square)
            self.board_controller.deselect_piece()
            self.board_controller.clear_held_piece()

    def create_move_piece(self, target):
        square = self.board_controller.game.find_square(target.piece)
        self.create_move_square(square)

    def create_move_square(self, square):
        selected_piece = self.board_controller.selected_piece.piece
        
        if self.board_controller.game.multiple_moves_exist(selected_piece, square):
            self.board_controller.create_promotion_picker(selected_piece, square)
        else:
            self.move = self.board_controller.game.find_move(selected_piece, square)

class AIChessInput(ChessInput):
    def get_move(self) -> Move | None:
        return pick_move(self.board_controller.game)

class NetworkChessInput(ChessInput):
    pass