import pygame.surface
from chess_board import ChessBoardObject
from move import Move
from tuple_n import TupleN


class ChessBoard:
    pass


class Piece(ChessBoardObject):
    def __init__(self, is_white: bool, **kwargs):
        super().__init__(**kwargs)
        self.white = is_white

    def is_white(self) -> bool:
        return self.white

    def is_empty(self):
        return False

    def handle_left_button_down(self):
        self.board.select_piece(self)

    def get_moves(self):
        return []


class Queen(Piece):
    def __init__(
        self,
        board: ChessBoard,
        is_white: bool,
        image: pygame.Surface,
        coords: tuple[int, int] = 0,
        dimensions: tuple[int, int] = 0,
        pos: tuple[int, int] = 0,
        depth: int = 0,
    ):
        super().__init__(
            board=board,
            is_white=is_white,
            coords=coords,
            dimensions=dimensions,
            depth=depth,
            pos=pos,
            image=image,
        )

    def move_piece(self):
        pass


class King(Piece):
    def __init__(
        self,
        board: ChessBoard,
        is_white: bool,
        image: pygame.Surface,
        coords: tuple[int, int] = 0,
        dimensions: tuple[int, int] = 0,
        pos: tuple[int, int] = 0,
        depth: int = 0,
    ):
        super().__init__(
            board=board,
            is_white=is_white,
            coords=coords,
            dimensions=dimensions,
            depth=depth,
            pos=pos,
            image=image,
        )

    def move_piece(self):
        pass


class Bishop(Piece):
    def __init__(
        self,
        board: ChessBoard,
        is_white: bool,
        image: pygame.Surface,
        coords: tuple[int, int] = 0,
        dimensions: tuple[int, int] = 0,
        pos: tuple[int, int] = 0,
        depth: int = 0,
    ):
        super().__init__(
            board=board,
            is_white=is_white,
            coords=coords,
            dimensions=dimensions,
            depth=depth,
            pos=pos,
            image=image,
        )

    def move_piece(self):
        pass


class Knight(Piece):
    def __init__(
        self,
        board: ChessBoard,
        is_white: bool,
        image: pygame.Surface,
        coords: tuple[int, int] = 0,
        dimensions: tuple[int, int] = 0,
        pos: tuple[int, int] = 0,
        depth: int = 0,
    ):
        super().__init__(
            board=board,
            is_white=is_white,
            coords=coords,
            dimensions=dimensions,
            depth=depth,
            pos=pos,
            image=image,
        )

    def move_piece(self):
        pass


class Rook(Piece):
    def __init__(
        self,
        board: ChessBoard,
        is_white: bool,
        image: pygame.Surface,
        coords: tuple[int, int] = 0,
        dimensions: tuple[int, int] = 0,
        pos: tuple[int, int] = 0,
        depth: int = 0,
    ):
        super().__init__(
            board=board,
            is_white=is_white,
            coords=coords,
            dimensions=dimensions,
            depth=depth,
            pos=pos,
            image=image,
        )

    def move_piece(self):
        pass


class Pawn(Piece):
    def __init__(
        self,
        board: ChessBoard,
        is_white: bool,
        image: pygame.Surface,
        coords: tuple[int, int] = 0,
        dimensions: tuple[int, int] = 0,
        pos: tuple[int, int] = 0,
        depth: int = 0,
    ):
        super().__init__(
            board=board,
            is_white=is_white,
            coords=coords,
            dimensions=dimensions,
            depth=depth,
            pos=pos,
            image=image,
        )

    def get_moves(self) -> list[Move]:
        valid_squares = []

        square = self.board.get_square(self)

        forward = (
            square + TupleN((-1, 0)) if self.is_white() else square + TupleN((1, 0))
        )
        left_diagonal = (
            square + TupleN((-1, -1)) if self.is_white() else square + TupleN((1, -1))
        )
        right_diagonal = (
            square + TupleN((-1, 1)) if self.is_white() else square + TupleN((1, -1))
        )

        square = self.board.get_piece(forward)
        if square.is_empty():
            valid_squares.append(square)

        square = self.board.get_piece(left_diagonal)
        if not square.is_empty() and square.is_white() != self.is_white():
            valid_squares.append(square)

        square = self.board.get_piece(right_diagonal)
        if not square.is_empty() and square.is_white() != self.is_white():
            valid_squares.append(square)

        return valid_squares
