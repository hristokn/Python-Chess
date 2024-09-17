from enum import Enum
from typing import Callable
from chess.squares import Square, Orientation, WhiteOrientation, BlackOrientation
from chess.move_logic import Move, pawn_move_logic, knight_move_logic, bishop_move_logic, rook_move_logic, king_move_logic, queen_move_logic

class PieceType(Enum):
    PAWN = 0
    KNIGHT = 1
    BISHOP = 2
    ROOK = 3
    KING = 4
    QUEEN = 5

    def __str__(self) -> str:
        match self:
            case PieceType.PAWN:
                return ''
            case PieceType.KNIGHT:
                return 'N'
            case PieceType.BISHOP:
                return 'B'
            case PieceType.ROOK:
                return 'R'
            case PieceType.KING:
                return 'K'
            case PieceType.QUEEN:
                return 'Q'
            case _:
                raise NotImplementedError

class Color(Enum):
    WHITE = 0
    BLACK = 1

class Piece:
    def __init__(self, color: Color, piece_type: PieceType):
        self.color = color
        self.type = piece_type

    def get_moves(self, square, prev_moves, chess_board):
        return get_logic(self.type)(square, chess_board, prev_moves, get_orientation(self.color))
    
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


def get_logic(piece_type: PieceType) -> Callable[[Square, dict[Square: Piece], Orientation], Move]: 
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
