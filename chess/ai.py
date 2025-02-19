from chess.chess import ChessBoard
from chess.enums import Color, PieceType
from random import randint
from time import sleep
from threading import Thread

class AIMove(Thread):
    def __init__(self, chess_board):
        Thread.__init__(self)
        self.runnable = pick_move
        self.chess_board = chess_board
        self.move = None

    def run(self):
        self.move = self.runnable(self.chess_board)


def pick_move(chess_board: ChessBoard):
    sleep(3)
    moves_count = len(chess_board.possible_moves)
    if moves_count == 0:
        return None
    return chess_board.possible_moves[randint(0, moves_count-1)]