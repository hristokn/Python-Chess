from enum import Enum
from abc import ABC
from chess.enums import Color

class Square(Enum):

    @classmethod
    def _missing_(cls, _):
        return Square.UNKNOWN

    def __str__(self) -> str:
        if self == Square.UNKNOWN:
            raise ValueError
        rank = int(self.value / 8) + 1
        result = str(rank)

        file = self.value % 8
        match file:
            case 0:
                result = 'a' + result
            case 1:
                result = 'b' + result
            case 2:
                result = 'c' + result
            case 3:
                result = 'd' + result
            case 4:
                result = 'e' + result
            case 5:
                result = 'f' + result
            case 6:
                result = 'g' + result
            case 7:
                result = 'h' + result

        return result


    def color(self):
        rank = int(self.value / 8)
        file = self.value % 8
        if (rank + file) % 2 == 0:
            return Color.WHITE
        return Color.BLACK


    def up(self):
        return WhiteOrientation.up(self)

    def down(self):
        return WhiteOrientation.down(self)

    def left(self):
        return WhiteOrientation.left(self)

    def right(self):
        return WhiteOrientation.right(self)

    def upleft(self):
        return WhiteOrientation.upleft(self)

    def upright(self):
        return WhiteOrientation.upright(self)

    def downleft(self):
        return WhiteOrientation.downleft(self)

    def downright(self):
        return WhiteOrientation.downright(self)

    A1 = 0
    A2 = 8
    A3 = 16
    A4 = 24
    A5 = 32
    A6 = 40
    A7 = 48
    A8 = 56
    B1 = 1
    B2 = 9
    B3 = 17
    B4 = 25
    B5 = 33
    B6 = 41
    B7 = 49
    B8 = 57
    C1 = 2
    C2 = 10
    C3 = 18
    C4 = 26
    C5 = 34
    C6 = 42
    C7 = 50
    C8 = 58
    D1 = 3
    D2 = 11
    D3 = 19
    D4 = 27
    D5 = 35
    D6 = 43
    D7 = 51
    D8 = 59
    E1 = 4
    E2 = 12
    E3 = 20
    E4 = 28
    E5 = 36
    E6 = 44
    E7 = 52
    E8 = 60
    F1 = 5
    F2 = 13
    F3 = 21
    F4 = 29
    F5 = 37
    F6 = 45
    F7 = 53
    F8 = 61
    G1 = 6
    G2 = 14
    G3 = 22
    G4 = 30
    G5 = 38
    G6 = 46
    G7 = 54
    G8 = 62
    H1 = 7
    H2 = 15
    H3 = 23
    H4 = 31
    H5 = 39
    H6 = 47
    H7 = 55
    H8 = 63
    UNKNOWN = 64

class Orientation(ABC):
    @staticmethod
    def up(square: Square):
        return NotImplementedError
    
    @staticmethod
    def down(square: Square):
        return NotImplementedError
    
    @staticmethod
    def left(square: Square):
        return NotImplementedError
    
    @staticmethod
    def right(square: Square):
        return NotImplementedError

    @staticmethod
    def upleft(square: Square):
        return NotImplementedError
    
    @staticmethod
    def upright(square: Square):
        return NotImplementedError
    
    @staticmethod
    def downleft(square: Square):
        return NotImplementedError
    
    @staticmethod
    def downright(square: Square):
        return NotImplementedError
    
    @staticmethod
    def _upleft(square: Square,
    orientation):
        return orientation.left(orientation.up(square))

    @staticmethod
    def _upright(square: Square,
    orientation):
        return orientation.right(orientation.up(square))
    
    @staticmethod
    def _downleft(square: Square,
    orientation):
        return orientation.left(orientation.down(square))
    
    @staticmethod
    def _downright(square: Square,
    orientation):
        return orientation.right(orientation.down(square))
    
class WhiteOrientation(Orientation):
    @staticmethod
    def up(square: Square):
        if square == Square.UNKNOWN:
            return Square.UNKNOWN
        return Square(square.value + 8)
    
    @staticmethod
    def down(square: Square):
        if square == Square.UNKNOWN:
            return Square.UNKNOWN
        return Square(square.value - 8)
    
    @staticmethod
    def left(square: Square):
        if square == Square.UNKNOWN:
            return Square.UNKNOWN
        if square  in [Square.A1, Square.A2, Square.A3, Square.A4,
                       Square.A5, Square.A6, Square.A7, Square.A8]:
            return Square.UNKNOWN
        return Square(square.value - 1)
    
    @staticmethod
    def right(square: Square):
        if square == Square.UNKNOWN:
            return Square.UNKNOWN
        if square  in [Square.H1, Square.H2, Square.H3, Square.H4,
                       Square.H5, Square.H6, Square.H7, Square.H8]:
            return Square.UNKNOWN
        return Square(square.value + 1)

    @staticmethod
    def upleft(square: Square):
        return super(__class__, __class__)._upleft(square,
    __class__)
    
    @staticmethod
    def upright(square: Square):
        return super(__class__, __class__)._upright(square,
    __class__)
    
    @staticmethod
    def downleft(square: Square):
        return super(__class__, __class__)._downleft(square,
    __class__)
    
    @staticmethod
    def downright(square: Square):
        return super(__class__, __class__)._downright(square,
    __class__)

class BlackOrientation(Orientation):
    @staticmethod
    def up(square: Square):
        if square == Square.UNKNOWN:
            return Square.UNKNOWN
        return Square(square.value - 8)
    
    @staticmethod
    def down(square: Square):
        if square == Square.UNKNOWN:
            return Square.UNKNOWN
        return Square(square.value + 8)
    
    @staticmethod
    def left(square: Square):
        if square == Square.UNKNOWN:
            return Square.UNKNOWN
        if square  in [Square.H1, Square.H2, Square.H3, Square.H4,
                       Square.H5, Square.H6,Square.H7, Square.H8]:
            return Square.UNKNOWN
        return Square(square.value + 1)
    
    @staticmethod
    def right(square: Square):
        if square == Square.UNKNOWN:
            return Square.UNKNOWN
        if square  in [Square.A1, Square.A2, Square.A3, Square.A4,
                       Square.A5, Square.A6, Square.A7, Square.A8]:
            return Square.UNKNOWN
        return Square(square.value - 1)
    
    @staticmethod
    def upleft(square: Square):
        return super(__class__, __class__)._upleft(square,
    __class__)
    
    @staticmethod
    def upright(square: Square):
        return super(__class__, __class__)._upright(square,
    __class__)
    
    @staticmethod
    def downleft(square: Square):
        return super(__class__, __class__)._downleft(square,
    __class__)
    
    @staticmethod
    def downright(square: Square):
        return super(__class__, __class__)._downright(square,
    __class__)