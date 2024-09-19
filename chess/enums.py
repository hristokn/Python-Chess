from enum import Enum

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
