from chess.chess import ChessBoard
from chess.enums import Color
from enum import Enum

class VictoryType(Enum):
    CHECKMATE = 0
    DRAW = 1
    TIMEOUT = 2

class FinishedGame:
    board: ChessBoard
    winner: Color | None
    victory_type: VictoryType
    def __init__(self, board: ChessBoard, winner: Color, victory_type: VictoryType):
        self.board = board
        self.winner = winner 
        self.victory_type = victory_type 