from chess.squares import Square
from chess.enums import Color, PieceType
from pygame import Surface
from pygame.image import load
from abc import ABC
from os.path import isfile

SQUARE_SIZE = 64
IMAGES = {
        'board': 'images/chess_board_1_white_side.png',
        'black_square': 'images/black_square_1.png',
        'white_square': 'images/white_square_1.png',
        'black_pawn': 'images/black_pawn.png',
        'black_rook': 'images/black_rook.png',
        'black_knight': 'images/black_knight.png',
        'black_bishop': 'images/black_bishop.png',
        'black_king': 'images/black_king.png',
        'black_queen': 'images/black_queen.png',
        'white_pawn': 'images/white_pawn.png',
        'white_rook': 'images/white_rook.png',
        'white_knight': 'images/white_knight.png',
        'white_bishop': 'images/white_bishop.png',
        'white_king': 'images/white_king.png',
        'white_queen': 'images/white_queen.png',
        'valid_move': 'images/valid_move.png',
        'valid_take': 'images/take.png'
        }

class ImageLibrary:
    def __init__(self, images: dict[str, str]):
        self.images = images
        self.loaded_images = {}
    
    def get(self, img_name: str):
        try:
            return self.loaded_images[img_name]
        except KeyError:
            img = loadImage(self.images[img_name])
            self.loaded_images[img_name] = img
            return img

class Drawable(ABC):
    def __init__(self, x1, y1, image: Surface):
        self.draw_x1 = x1
        self.draw_y1 = y1 
        self.image = image

    def draw(self, surface: Surface):
        if self.image != None:
            surface.blit(self.image, (self.draw_x1,self.draw_y1))


def loadImage(fileName):
    if isfile(fileName):
        image = load(fileName)
        image = image.convert_alpha()
        return image
    else:
        raise Exception(f"Error loading image: {fileName} – Check filename and path?")

def get_square_pos(board_x, board_y, square: Square, color: Color) -> tuple[int, int]:
    x = board_x
    y = board_y
    rank = int(square.value / 8)
    file = square.value % 8
    if color == Color.WHITE:
        x = x + SQUARE_SIZE * file
        y = y + SQUARE_SIZE * (7 - rank)
    elif color == Color.BLACK:
        x = x + SQUARE_SIZE * (7 - file)
        y = y + SQUARE_SIZE * rank

    return (x,y)

def get_square_color(square: Square):
    rank = int(square.value / 8)
    file = square.value % 8
    if (rank + file) % 2 == 0:
        return True
    return False

def get_piece_image_name(color: Color, type: PieceType):
    match color, type:
        case Color.WHITE, PieceType.PAWN:
            return "white_pawn"
        case Color.WHITE, PieceType.KNIGHT:
            return "white_knight"
        case Color.WHITE, PieceType.ROOK:
            return "white_rook"
        case Color.WHITE, PieceType.BISHOP:
            return "white_bishop"
        case Color.WHITE, PieceType.QUEEN:
            return "white_queen"
        case Color.WHITE, PieceType.KING:
            return "white_king"
        case Color.BLACK, PieceType.PAWN:
            return "black_pawn"
        case Color.BLACK, PieceType.KNIGHT:
            return "black_knight"
        case Color.BLACK, PieceType.ROOK:
            return "black_rook"
        case Color.BLACK, PieceType.BISHOP:
            return "black_bishop"
        case Color.BLACK, PieceType.QUEEN:
            return "black_queen"
        case Color.BLACK, PieceType.KING:
            return "black_king"
        case _, _:
            raise NotImplementedError