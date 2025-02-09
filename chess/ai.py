from chess.chess import ChessBoard
from chess.enums import Color, PieceType
from random import randint


def pick_move(chess_board: ChessBoard):
    moves_count = len(chess_board.possible_moves)
    if moves_count == 0:
        return None
    return chess_board.possible_moves[randint(0, moves_count-1)]