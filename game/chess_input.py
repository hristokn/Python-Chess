from chess.moves import Move
from chess.enums import Color
from chess.ai import AIMove
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


class Premove:
    def __init__(self, starting_square, ending_square, piece):
        self.starting_square = starting_square
        self.ending_square = ending_square
        self.piece = piece


class MouseChessInput(ChessInput):
    def __init__(self, board_controller, colors: list[Color]) -> None:
        super().__init__(board_controller)
        self.move = None
        self.premove = None
        self.colors = colors

    def get_move(self) -> Move | None:
        if self.premove != None:
            self.waiting_for_move = False
            return self.use_premove()
        elif self.move == None:
            self.waiting_for_move = True
            return None
        elif self.move != None:
            self.waiting_for_move = False
            _move = self.move
            self.move = None
            return _move

    def update(self):
        self.handle_clicked_pieces()

    def handle_clicked_pieces(self):
        _piecedown = None
        _pieceup = None
        _squaredown = None
        _squareup = None
        for piece in self.board_controller.piece_controllers:
            if piece.left_buttop_down:
                _piecedown = piece
            if piece.left_buttop_up:
                _pieceup = piece

        for square in self.board_controller.square_controllers:
            if square.left_buttop_down:
                _squaredown = square
            if square.left_buttop_up:
                _squareup = square

        if _piecedown != None:
            self.piecedown(_piecedown)
            _piecedown.left_buttop_down = False

        if _pieceup != None:
            self.pieceup(_pieceup)
            _pieceup.left_buttop_up = False

        if _squaredown != None:
            self.squaredown(_squaredown)
            _squaredown.left_buttop_down = False

        if _squareup != None:
            self.squareup(_squareup)
            _squareup.left_buttop_up = False

    def piecedown(self, piece):
        if (
            self.board_controller.selected_piece == None
            and piece.piece.color in self.colors
        ):
            self.board_controller.select_piece(piece)
            self.board_controller.set_held_piece(piece)
        elif (
            self.board_controller.selected_piece == piece
            and piece.piece.color in self.colors
        ):
            self.board_controller.set_held_piece(piece)
        elif self.board_controller.selected_piece != None:
            self.create_move_piece(piece)

    def squaredown(self, square):
        if (
            self.board_controller.selected_piece != None
            and self.board_controller.selected_piece.piece.color in self.colors
        ):
            self.create_move_square(square.square)
        if self.board_controller.selected_piece == None and self.premove != None:
            self.remove_premove()

    def pieceup(self, piece):
        if self.board_controller.selected_piece == piece:
            self.board_controller.clear_held_piece()
        elif (
            self.board_controller.selected_piece != None
            and self.board_controller.held_piece != None
            and self.board_controller.selected_piece.piece.color in self.colors
        ):
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

        if self.premove != None:
            self.remove_premove()

        if self.board_controller.game.multiple_moves_exist(selected_piece, square):
            self.board_controller.create_promotion_picker(selected_piece, square)
        elif self.waiting_for_move:
            self.move = self.board_controller.game.find_move(selected_piece, square)
        else:
            self.save_premove(selected_piece, square)

    def save_premove(self, piece, square):
        self.premove = Premove(
            self.board_controller.game.find_square(piece), square, piece
        )
        self.board_controller.highlight_square(self.premove.starting_square)
        self.board_controller.highlight_square(self.premove.ending_square)

    def remove_premove(self):
        if self.premove != None:
            self.board_controller.unhighlight_square(self.premove.starting_square)
            self.board_controller.unhighlight_square(self.premove.ending_square)
            self.premove = None

    def use_premove(self) -> Move:
        if self.premove == None:
            raise ValueError(
                "Premove is None, cannot use a premove that does not exist."
            )
        _premove_piece = self.premove.piece
        _premove_square = self.premove.ending_square
        self.remove_premove()
        return self.board_controller.game.find_move(_premove_piece, _premove_square)


class AIChessInput(ChessInput):
    thread = None
    move = None

    def __init__(self, board_controller, color):
        super().__init__(board_controller)
        self.color = color

    def get_move(self) -> Move | None:
        if self.move == None and self.thread == None:
            self.thread = AIMove(self.board_controller.game, self.color)
            self.thread.start()
            self.waiting_for_move = True
            return None
        elif self.move != None:
            _move = self.move
            self.move = None
            self.waiting_for_move = False
            return _move
        else:
            return None

    def update(self):
        if self.waiting_for_move and self.thread != None and not self.thread.is_alive():
            self.move = self.thread.move
            self.thread = None
            self.waiting_for_move = False
        else:
            pass


class NetworkChessInput(ChessInput):
    pass
