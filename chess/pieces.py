from typing import Callable
from chess.squares import Square, Orientation, WhiteOrientation, BlackOrientation
from chess.move_logic import (
    Move,
    pawn_move_logic,
    knight_move_logic,
    bishop_move_logic,
    rook_move_logic,
    king_move_logic,
    queen_move_logic,
)
from chess.enums import Color, PieceType


class Piece:
    def __init__(self, color: Color, piece_type: PieceType):
        self.color = color
        self.type = piece_type
        self.orientation = get_orientation(color)

    def get_moves(self, square, prev_moves, chess_board):
        return get_logic(self.type)(square, chess_board, prev_moves, self.orientation)

    def __str__(self) -> str:
        return str(self.type)


def get_orientation(color: Color):
    match color:
        case Color.WHITE:
            return WhiteOrientation
        case Color.BLACK:
            return BlackOrientation
        case _:
            raise NotImplementedError


def get_logic(
    piece_type: PieceType,
) -> Callable[[Square, dict[Square:Piece], Orientation], Move]:
    match piece_type:
        case PieceType.PAWN:
            return pawn_move_logic
        case PieceType.KNIGHT:
            return knight_move_logic
        case PieceType.BISHOP:
            return bishop_move_logic
        case PieceType.ROOK:
            return rook_move_logic
        case PieceType.QUEEN:
            return queen_move_logic
        case PieceType.KING:
            return king_move_logic
        case _:
            raise NotImplementedError
