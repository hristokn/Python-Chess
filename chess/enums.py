from enum import Enum


class ExtendedEnum(Enum):

    @classmethod
    def list(cls):
        return [e for e in cls]


class PieceType(ExtendedEnum):
    PAWN = 0
    KNIGHT = 1
    BISHOP = 2
    ROOK = 3
    KING = 4
    QUEEN = 5

    def __str__(self) -> str:
        match self:
            case PieceType.PAWN:
                return ""
            case PieceType.KNIGHT:
                return "N"
            case PieceType.BISHOP:
                return "B"
            case PieceType.ROOK:
                return "R"
            case PieceType.KING:
                return "K"
            case PieceType.QUEEN:
                return "Q"
            case _:
                raise NotImplementedError


class Color(ExtendedEnum):
    WHITE = 0
    BLACK = 1

    def next(self):
        if self == Color.WHITE:
            return Color.BLACK
        elif self == Color.BLACK:
            return Color.WHITE

    def previous(self):
        if self == Color.WHITE:
            return Color.BLACK
        elif self == Color.BLACK:
            return Color.WHITE
