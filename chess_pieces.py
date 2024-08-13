import pygame.surface
from chess_board import ChessBoardObject
from move import Move
from tuple_n import TupleN
from my_enums import Color


class ChessBoard:
    pass


class Piece(ChessBoardObject):
    def __init__(self, color: Color, **kwargs):
        super().__init__(**kwargs)
        self.color = color

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

    def get_moves(
        self, square: TupleN[int, int], chess_board: list[ChessBoardObject]
    ) -> list[Move]:
        valid_squares = []

        try:
            forward_square = (
                square + TupleN((-1, 0))
                if self.color == Color.WHITE
                else square + TupleN((1, 0))
            )
            piece = chess_board[forward_square[0]][forward_square[1]]
            if piece.is_empty():
                valid_squares.append(Move(square, forward_square))
        except IndexError:
            pass

        try:
            left_diagonal_square = (
                square + TupleN((-1, -1))
                if self.color == Color.WHITE
                else square + TupleN((1, -1))
            )
            piece = chess_board[left_diagonal_square[0]][left_diagonal_square[1]]
            if not piece.is_empty() and self.color != piece.color:
                valid_squares.append(Move(square, left_diagonal_square))
        except IndexError:
            pass

        try:
            right_diagonal_square = (
                square + TupleN((-1, 1))
                if self.color == Color.WHITE
                else square + TupleN((1, -1))
            )
            piece = chess_board[right_diagonal_square[0]][right_diagonal_square[1]]
            if not piece.is_empty() and self.color != piece.color:
                valid_squares.append(Move(square, right_diagonal_square))
        except IndexError:
            pass

        return valid_squares
