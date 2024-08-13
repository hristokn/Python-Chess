import pygame.surface
from game_objects import Collider, GameObject, Drawable, ChessBoardObject
from chess_pieces import Pawn, Rook, Knight, Bishop, King, Queen
from tuple_n import TupleN
from move import Move
from my_enums import Color


class ChessBoard(Collider, GameObject, Drawable):
    def __init__(
        self,
        coords: tuple[int, int],
        dimensions: tuple[int, int],
        image: pygame.Surface,
        pos: tuple[int, int],
        game_images: dict[str, pygame.Surface],
        game_custom_events: dict[str, int],
        depth: int = -10,
    ):
        super().__init__(
            coords=coords, dimensions=dimensions, depth=depth, pos=pos, image=image
        )
        self.game_images = game_images
        self.game_custom_events = game_custom_events
        self.chess_board = []
        self.objects = []
        self._fill_board()
        self.selected = None
        self.past_moves = []
        self.possible_moves = []
        self.color_to_move = Color.WHITE
        self.taken_pieces = []

    def _fill_board(self):

        for row in range(8):
            self.chess_board.append([])
            for column in range(8):
                self.chess_board[row].append(None)
                self.add_empty_square((row, column))

        rook = Rook(self, False, self.game_images["black_rook"])
        self._fill_square([0, 0], rook)
        rook = Rook(self, False, self.game_images["black_rook"])
        self._fill_square([0, 7], rook)

        bishop = Bishop(self, False, self.game_images["black_bishop"])
        self._fill_square([0, 1], bishop)
        bishop = Bishop(self, False, self.game_images["black_bishop"])
        self._fill_square([0, 6], bishop)

        knight = Knight(self, False, self.game_images["black_knight"])
        self._fill_square([0, 2], knight)
        knight = Knight(self, False, self.game_images["black_knight"])
        self._fill_square([0, 5], knight)

        queen = Queen(self, False, self.game_images["black_queen"])
        self._fill_square([0, 3], queen)
        king = King(self, False, self.game_images["black_king"])
        self._fill_square([0, 4], king)

        for column in range(8):
            pawn = Pawn(self, False, self.game_images["black_pawn"])
            self._fill_square([1, column], pawn)

        rook = Rook(self, True, self.game_images["white_rook"])
        self._fill_square([7, 0], rook)
        rook = Rook(self, True, self.game_images["white_rook"])
        self._fill_square([7, 7], rook)

        bishop = Bishop(self, True, self.game_images["white_bishop"])
        self._fill_square([7, 1], bishop)
        bishop = Bishop(self, True, self.game_images["white_bishop"])
        self._fill_square([7, 6], bishop)

        knight = Knight(self, True, self.game_images["white_knight"])
        self._fill_square([7, 2], knight)
        knight = Knight(self, True, self.game_images["white_knight"])
        self._fill_square([7, 5], knight)

        queen = Queen(self, True, self.game_images["white_queen"])
        self._fill_square([7, 3], queen)
        king = King(self, True, self.game_images["white_king"])
        self._fill_square([7, 4], king)

        for column in range(8):
            pawn = Pawn(self, True, self.game_images["white_pawn"])
            self._fill_square([6, column], pawn)

        for row in self.chess_board:
            for square in row:
                self._add_object(square)

    def _convert_square_to_screen_position(self, square: tuple[int, int]):
        dimensions = (self.dimensions[0] / 8, self.dimensions[1] / 8)
        coords = (
            self.coords[0] + square[1] * dimensions[0],
            self.coords[1] + square[0] * dimensions[1],
        )

        return (coords, dimensions)

    def _fill_square(self, square: tuple[int, int], object: ChessBoardObject):
        empty_square = self.chess_board[square[0]][square[1]]
        object.coords = empty_square.coords
        object.dimensions = empty_square.dimensions
        object.pos = empty_square.pos
        self.chess_board[square[0]][square[1]] = object

    def add_empty_square(self, square):
        screen_pos = self._convert_square_to_screen_position(square)
        object = EmptySquare(self, screen_pos[0], screen_pos[1])
        self.chess_board[square[0]][square[1]] = object

    def _remove_object(self, object: GameObject):
        event_data = {"object": object}
        pygame.event.post(
            pygame.event.Event(self.game_custom_events["object_removed"], event_data)
        )

    def _add_object(self, object: GameObject):
        event_data = {"object": object}
        pygame.event.post(
            pygame.event.Event(self.game_custom_events["object_created"], event_data)
        )

    def get_square(self, piece: ChessBoardObject) -> TupleN | None:
        rowIndex = -1
        columnIndex = -1
        for row in self.chess_board:
            rowIndex += 1
            columnIndex = -1
            for column in row:
                columnIndex += 1
                if column == piece:
                    return TupleN((rowIndex, columnIndex))
        return None

    def get_piece(self, square: TupleN[int, int]) -> ChessBoardObject:
        return self.chess_board[square[0]][square[1]]

    def get_selected_piece(self):
        return self.selected

    def select_piece(self, piece: ChessBoardObject):
        self.deselect_piece()
        if piece.is_empty():
            return

        self.selected = piece
        self.highlight_potential_moves()

    def highlight_potential_moves(self, piece: ChessBoardObject | None = None):
        if piece == None:
            piece = self.selected
        if piece.is_empty():
            raise Exception("Empty square passed as argument")

        square = self.get_square(piece)
        valid_moves = filter(lambda move: move.start == square, self.possible_moves)
        for move in valid_moves:
            piece = self.get_piece(move.end)
            if piece.is_empty():
                self.add_valid_move_object(move)
            else:
                self.add_valid_take_object(move)

    def add_valid_move_object(self, square: tuple[int, int]):
        screen_position = self._convert_square_to_screen_position(square)
        move = ValidMove(
            self,
            screen_position[0],
            screen_position[1],
            self.game_images["valid_move_symbol"],
            screen_position[0],
        )
        self.objects.append(move)
        self._add_object(move)

    def add_valid_take_object(self, square: tuple[int, int]):
        screen_position = self._convert_square_to_screen_position(square)
        take = ValidTake(
            self,
            screen_position[0],
            screen_position[1],
            self.game_images["take_symbol"],
            screen_position[0],
        )
        self.objects.append(take)
        self._add_object(take)

    def deselect_piece(self):
        self.selected = None
        for object in self.objects:
            self._remove_object(object)
        self.objects = []

    def get_square_by_pixel(self, pos: tuple[int, int]):
        square_size = self.dimensions[0] / self.chess_board.count()
        relative_pos = self.pos - pos
        row = relative_pos[0] / square_size
        column = relative_pos[1] / square_size
        return (row, column)

    def next_player(self):
        self.color_to_move = (
            Color.BLACK if self.color_to_move == Color.WHITE else Color.WHITE
        )

    def calculate_potential_moves(self, color: Color | None = None):
        self.moves = []
        if color == None:
            color = self.color

        for row in ChessBoard:
            for piece in row:
                if not piece.is_empty() and piece.color == color:
                    self.possible_moves += piece.get_moves(
                        self.get_square(piece), self.chess_board
                    )

    def play_move(self, move: Move):
        if not move in self.possible_moves:
            raise Exception("Tried to play invalid move")

        if self.get_piece(move.end).is_empty():
            self.move(move)
        else:
            self.take(move)

        self.past_moves.append(move)
        self.next_player()
        self.calculate_potential_moves()

    def move(self, move: Move):
        start_piece = self.get_piece(move.start)
        end_square = self.get_piece(move.end)
        self.chess_board[move.end[0]][move.end[1]] = start_piece
        self.chess_board[move.start[0]][move.start[1]] = end_square

    def take(self, move: Move):
        start_piece = self.get_piece(move.start)
        end_piece = self.get_piece(move.end)

        self.chess_board[move.end[0]][move.end[1]] = start_piece
        self.add_empty_square(move.start)
        self._add_object(self.chess_board[move.start[0]][move.start[1]])
        self._remove_object(end_piece)
        self.taken_pieces.append(end_piece)


class EmptySquare(ChessBoardObject):
    def __init__(
        self,
        board: ChessBoard,
        coords: tuple[int, int],
        dimensions: tuple[int, int],
        depth: int = -9,
    ):
        super().__init__(
            board=board,
            coords=coords,
            dimensions=dimensions,
            depth=depth,
            pos=coords,
        )

    def handle_left_button_down(self):
        """deselect piece"""


class ValidMove(ChessBoardObject):
    def __init__(
        self,
        board: ChessBoard,
        coords: tuple[int, int],
        dimensions: tuple[int, int],
        image: pygame.surface,
        pos: tuple[int, int],
        depth: int = 1,
    ):
        super().__init__(
            board=board,
            coords=coords,
            dimensions=dimensions,
            depth=depth,
            pos=pos,
            image=image,
        )

    def handle_left_button_down(self):
        """'move"""

    def handle_left_button_up(self):
        """'move"""


class ValidTake(ChessBoardObject):
    def __init__(
        self,
        board: ChessBoard,
        coords: tuple[int, int],
        dimensions: tuple[int, int],
        image: pygame.surface,
        pos: tuple[int, int],
        depth: int = 1,
    ):
        super().__init__(
            board=board,
            coords=coords,
            dimensions=dimensions,
            depth=depth,
            pos=pos,
            image=image,
        )

    def handle_left_button_down(self):
        """'take"""

    def handle_left_button_up(self):
        """'take"""
