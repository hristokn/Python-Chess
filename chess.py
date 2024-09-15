from enum import Enum
from typing import Any
from chess_pieces import Pawn
from my_enums import Color


class Square(Enum):
    def up(self):
        return Square(self.value + 8)

    def down(self):
        return Square(self.value - 8)

    def right(self):
        if self.value % 8 == 7:
            raise ValueError
        else:    
            return Square(self.value + 1)
    def left(self):
        pass
    def upright(self):
        pass
    def upleft(self):
        pass
    def downright(self):
        pass
    def downleft(self):
        pass
    A1 = 0, A2 = 8, A3 = 16, A4 = 24, A5 = 32, A6 = 40 ,A7 = 48 ,A8 = 56
    B1 = 1 ,B2 = 9 ,B3 = 17 ,B4 = 25 ,B5 = 33 ,B6 = 41 ,B7 = 49 ,B8 = 57
    C1 = 2 ,C2 = 10 ,C3 = 18 ,C4 = 26 ,C5 = 34 ,C6 = 42 ,C7 = 50 ,C8 = 58
    D1 = 3 ,D2 = 11 ,D3 = 19 ,D4 = 27 ,D5 = 35 ,D6 = 43 ,D7 = 51 ,D8 = 59
    E1 = 4 ,E2 = 12 ,E3 = 20 ,E4 = 28 ,E5 = 36 ,E6 = 44 ,E7 = 52 ,E8 = 60
    F1 = 5 ,F2 = 13 ,F3 = 21 ,F4 = 29 ,F5 = 37 ,F6 = 45 ,F7 = 53 ,F8 = 61
    G1 = 6 ,G2 = 14 ,G3 = 22 ,G4 = 30 ,G5 = 38 ,G6 = 46 ,G7 = 54 ,G8 = 62
    H1 = 7 ,H2 = 15 ,H3 = 23 ,H4 = 31 ,H5 = 39 ,H6 = 47 ,H7 = 55 ,H8 = 63


class ChessBoard:
    def __init__(self):
        self.board = {}

    def _fill_board(self):
        for square in Square:
            self.board[square] = None

def standard_board(board):
        for square in Square:
            board[square] = None

class PieceLogic:
    def get_moves(self, square: Square, board: ChessBoard):
        return NotImplementedError

class Piece:
    def __init__(self, color: Color):
        self.color = color
        self._piece_logic = PieceLogic()

    def get_moves(self, square: Square, board: ChessBoard):
        return self._piece_logic.get_moves(square, board)

class Move:
    def __init__(self, changes: dict[Square: Piece], taken: list[Piece]):
        self.changes = changes
        self.taken = taken

class Pawn(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        if color == Color.WHITE:
            self._piece_logic = WhitePawnLogic()
        elif color == Color.BLACK:
            self._piece_logic = BlackPawnLogic()

class WhitePawnLogic(PieceLogic):
    def get_moves(self, square: Square, board: ChessBoard):
        piece = board[square]
        moves = []
        forward = board[square.up()] 
        if forward == None:
            changes = {square: None, square.up(): piece}
            moves.append(Move(changes, []))

        diagonal = board[square.upleft()]
        if diagonal != None and diagonal.color != piece.color:
            changes = {square: None, square.upleft(): piece}
            taken = [diagonal]
            moves.append(changes, taken)

        diagonal = board[square.upright()]
        if diagonal != None and diagonal.color != piece.color:
            changes = {square: None, square.upright(): piece}
            taken = [diagonal]
            moves.append(changes, taken)

        return moves

class BlackPawnLogic(Piece):
    def get_moves(self, square: Square, board: ChessBoard):
        piece = board[square]
        moves = []
        forward = board[square.up()] 
        if forward == None:
            changes = {square: None, square.down(): piece}
            moves.append(Move(changes, []))

        diagonal = board[square.downleft()]
        if diagonal != None and diagonal.color != piece.color:
            changes = {square: None, square.downleft(): piece}
            taken = [diagonal]
            moves.append(changes, taken)

        diagonal = board[square.downright()]
        if diagonal != None and diagonal.color != piece.color:
            changes = {square: None, square.downright(): piece}
            taken = [diagonal]
            moves.append(changes, taken)

        return moves

