# Example file showing a basic pygame "game loop"
import pygame
from pygame_extra import *
from enum import Enum
from game import Game
from chess_board import ChessBoard

board = [
    [
        Piece.B_ROOK,
        Piece.B_KNIGHT,
        Piece.B_BISHOP,
        Piece.B_QUEEN,
        Piece.B_KING,
        Piece.B_BISHOP,
        Piece.B_KNIGHT,
        Piece.B_ROOK,
    ],
    [
        Piece.B_PAWN,
        Piece.B_PAWN,
        Piece.B_PAWN,
        Piece.B_PAWN,
        Piece.B_PAWN,
        Piece.B_PAWN,
        Piece.B_PAWN,
        Piece.B_PAWN,
    ],
    [],
    [],
    [],
    [],
    [
        Piece.W_PAWN,
        Piece.W_PAWN,
        Piece.W_PAWN,
        Piece.W_PAWN,
        Piece.W_PAWN,
        Piece.W_PAWN,
        Piece.W_PAWN,
        Piece.W_PAWN,
    ],
    [
        Piece.W_ROOK,
        Piece.W_KNIGHT,
        Piece.W_BISHOP,
        Piece.W_KING,
        Piece.W_QUEEN,
        Piece.W_BISHOP,
        Piece.W_KNIGHT,
        Piece.W_ROOK,
    ],
]

# piece_images = {
#     Piece.W_PAWN: loadImage("images/white_pawn.png"),
#     Piece.W_ROOK: loadImage("images/white_rook.png"),
#     Piece.W_BISHOP: loadImage("images/white_bishop.png"),
#     Piece.W_KNIGHT: loadImage("images/white_knight.png"),
#     Piece.W_QUEEN: loadImage("images/white_queen.png"),
#     Piece.W_KING: loadImage("images/white_king.png"),
#     Piece.B_PAWN: loadImage("images/black_pawn.png"),
#     Piece.B_ROOK: loadImage("images/black_rook.png"),
#     Piece.B_BISHOP: loadImage("images/black_bishop.png"),
#     Piece.B_KNIGHT: loadImage("images/black_knight.png"),
#     Piece.B_QUEEN: loadImage("images/black_queen.png"),
#     Piece.B_KING: loadImage("images/black_king.png"),
# }

# board_image = loadImage("images/chessBoard1.png")

game = Game(1280, 640)

# board = ChessBoard((100, 100), (512, 512), board_image, (100, 100), game.image_library)

# game.add_object(board)
game.run()
