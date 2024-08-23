import pygame.surface
from chess_board import ChessBoardObject
from move import Move
from tuple_n import TupleN
from my_enums import Color


class Piece(ChessBoardObject):
    def __init__(self, color: Color, **kwargs):
        super().__init__(**kwargs)
        self.color = color
        self.has_moved = False

    def is_empty(self):
        return False

    def handle_left_button_down(self):
        self.board.select_piece(self)

    def get_moves(self, chess_board: list[list[ChessBoardObject]]) -> list[Move]:
        return []

    def move(self, square: TupleN[int, int], screen_coords: TupleN[int, int]):
        super().move(square, screen_coords)
        self.has_moved = True


class Queen(Piece):
    def __init__(
        self,
        color: Color,
        image: pygame.Surface,
        square: TupleN[int, int],
        coords: tuple[int, int] = 0,
        dimensions: tuple[int, int] = 0,
        pos: tuple[int, int] = 0,
        depth: int = 0,
    ):
        super().__init__(
            square=square,
            color=color,
            coords=coords,
            dimensions=dimensions,
            depth=depth,
            pos=pos,
            image=image,
        )


class King(Piece):
    def __init__(
        self,
        color: Color,
        image: pygame.Surface,
        square: TupleN[int, int],
        coords: tuple[int, int] = 0,
        dimensions: tuple[int, int] = 0,
        pos: tuple[int, int] = 0,
        depth: int = 0,
    ):
        super().__init__(
            square=square,
            color=color,
            coords=coords,
            dimensions=dimensions,
            depth=depth,
            pos=pos,
            image=image,
        )


class Bishop(Piece):
    def __init__(
        self,
        color: Color,
        image: pygame.Surface,
        square: TupleN[int, int],
        coords: tuple[int, int] = 0,
        dimensions: tuple[int, int] = 0,
        pos: tuple[int, int] = 0,
        depth: int = 0,
    ):
        super().__init__(
            square=square,
            color=color,
            coords=coords,
            dimensions=dimensions,
            depth=depth,
            pos=pos,
            image=image,
        )


class Knight(Piece):
    def __init__(
        self,
        color: Color,
        image: pygame.Surface,
        square: TupleN[int, int],
        coords: tuple[int, int] = 0,
        dimensions: tuple[int, int] = 0,
        pos: tuple[int, int] = 0,
        depth: int = 0,
    ):
        super().__init__(
            square=square,
            color=color,
            coords=coords,
            dimensions=dimensions,
            depth=depth,
            pos=pos,
            image=image,
        )


class Rook(Piece):
    def __init__(
        self,
        color: Color,
        image: pygame.Surface,
        square: TupleN[int, int],
        coords: tuple[int, int] = 0,
        dimensions: tuple[int, int] = 0,
        pos: tuple[int, int] = 0,
        depth: int = 0,
    ):
        super().__init__(
            color=color,
            coords=coords,
            dimensions=dimensions,
            depth=depth,
            pos=pos,
            image=image,
            square=square,
        )


class Pawn(Piece):
    def __init__(
        self,
        color: Color,
        image: pygame.Surface,
        square: TupleN[int, int],
        coords: tuple[int, int] = 0,
        dimensions: tuple[int, int] = 0,
        pos: tuple[int, int] = 0,
        depth: int = 0,
    ):
        super().__init__(
            color=color,
            coords=coords,
            dimensions=dimensions,
            depth=depth,
            pos=pos,
            image=image,
            square=square,
        )

    def get_moves(self, chess_board: list[list[ChessBoardObject]]) -> list[Move]:
        valid_squares = []

        try:
            forward_square = (
                self.square + TupleN((-1, 0))
                if self.color == Color.WHITE
                else self.square + TupleN((1, 0))
            )
            piece = chess_board[forward_square[0]][forward_square[1]]
            if piece.is_empty():
                valid_squares.append(Move(self.square, forward_square))
        except IndexError:
            pass

        try:
            left_diagonal_square = (
                self.square + TupleN((-1, -1))
                if self.color == Color.WHITE
                else self.square + TupleN((1, -1))
            )
            piece = chess_board[left_diagonal_square[0]][left_diagonal_square[1]]
            if not piece.is_empty() and self.color != piece.color:
                valid_squares.append(Move(self.square, left_diagonal_square))
        except IndexError:
            pass

        try:
            right_diagonal_square = (
                self.square + TupleN((-1, 1))
                if self.color == Color.WHITE
                else self.square + TupleN((1, -1))
            )
            piece = chess_board[right_diagonal_square[0]][right_diagonal_square[1]]
            if not piece.is_empty() and self.color != piece.color:
                valid_squares.append(Move(self.square, right_diagonal_square))
        except IndexError:
            pass

        return valid_squares
