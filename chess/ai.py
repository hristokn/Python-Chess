from chess.chess import ChessBoard
from chess.enums import Color, PieceType
from random import randint


def pick_move(chess_board: ChessBoard):
    return chess_board.possible_moves[randint(0, len(chess_board.possible_moves)-1)]