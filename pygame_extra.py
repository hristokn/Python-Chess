import pygame
import os
from enum import Enum

Piece = Enum(
    "Enum",
    [
        "W_PAWN",
        "W_ROOK",
        "W_BISHOP",
        "W_KNIGHT",
        "W_QUEEN",
        "W_KING",
        "B_PAWN",
        "B_ROOK",
        "B_BISHOP",
        "B_KNIGHT",
        "B_QUEEN",
        "B_KING",
    ],
)


def loadImage(fileName):
    if os.path.isfile(fileName):
        image = pygame.image.load(fileName)
        image = image.convert_alpha()
        return image
    else:
        raise Exception(f"Error loading image: {fileName} – Check filename and path?")


def draw_board(board_image, board, piece_images, screen):
    BOARD_X = 100
    BOARD_Y = 100
    CHESS_PIECE_SIZE = 64
    screen.blit(board_image, (BOARD_X, BOARD_Y))

    row_number = -1
    column_number = -1
    for row in board:
        row_number += 1
        column_number = -1
        for square in row:
            column_number += 1
            if square in Piece:
                screen.blit(
                    piece_images[square],
                    (
                        BOARD_X + column_number * CHESS_PIECE_SIZE,
                        BOARD_Y + row_number * CHESS_PIECE_SIZE,
                    ),
                )
