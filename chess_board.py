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
        self.chess_board: list[list[ChessBoardObject]] = []
        self.objects = []
        self.selected_piece = None
        self.past_moves = []
        self.possible_moves = []
        self.color_to_move = Color.WHITE
        self.taken_pieces = []

        self._fill_board()
        self.calculate_potential_moves()

    def update(self):
        super().update()
        for row in self.chess_board:
            for obj in row:
                click = obj.pop_click()
                if click == None:
                    continue
                elif click.button == 1:
                    if obj.is_empty():
                        self.square_clicked(obj, click)
                    else:
                        self.piece_clicked(obj, click)
        for obj in self.objects:
            click = obj.pop_click()
            if click == None:
                continue
            elif click.type == pygame.MOUSEBUTTONUP and click.button == 1:
                self.obj_clicked(obj, click)
            elif click.type == pygame.MOUSEBUTTONDOWN:
                pass
            else:
                raise ValueError

    def obj_clicked(self, obj, click):
        # left click on piece, up or down
        move_start = self.selected_piece.square
        move_end = obj.square
        move = Move(move_start, move_end)
        self.selected_piece = None
        self.play_move(move)

    def square_clicked(self, obj, click):
        downclick = click.type == pygame.MOUSEBUTTONDOWN
        if downclick:
            if self.selected_piece == None:
                pass
            else:
                self.deselect_piece()

    def piece_clicked(self, piece, click):
        # left click on piece, up or down
        downclick = click.type == pygame.MOUSEBUTTONDOWN
        if downclick:
            if self.selected_piece == piece:
                pass
            else:
                self.select_piece(piece)
        else:
            if self.selected_piece == piece:
                pass
            else:
                pass

    def _fill_board(self):

        for row in range(8):
            self.chess_board.append([])
            for column in range(8):
                self.chess_board[row].append(None)
                self.add_empty_square(TupleN((row, column)))

        rook = Rook(Color.BLACK, self.game_images["black_rook"], TupleN((0, 0)))
        self._fill_square(rook)
        rook = Rook(Color.BLACK, self.game_images["black_rook"], TupleN((0, 7)))
        self._fill_square(rook)

        bishop = Bishop(Color.BLACK, self.game_images["black_bishop"], TupleN((0, 1)))
        self._fill_square(bishop)
        bishop = Bishop(Color.BLACK, self.game_images["black_bishop"], TupleN((0, 6)))
        self._fill_square(bishop)

        knight = Knight(Color.BLACK, self.game_images["black_knight"], TupleN((0, 2)))
        self._fill_square(knight)
        knight = Knight(Color.BLACK, self.game_images["black_knight"], TupleN((0, 5)))
        self._fill_square(knight)

        queen = Queen(Color.BLACK, self.game_images["black_queen"], TupleN((0, 3)))
        self._fill_square(queen)
        king = King(Color.BLACK, self.game_images["black_king"], TupleN((0, 4)))
        self._fill_square(king)

        for column in range(8):
            pawn = Pawn(
                Color.BLACK, self.game_images["black_pawn"], TupleN((1, column))
            )
            self._fill_square(pawn)

        rook = Rook(Color.WHITE, self.game_images["white_rook"], TupleN((7, 0)))
        self._fill_square(rook)
        rook = Rook(Color.WHITE, self.game_images["white_rook"], TupleN((7, 7)))
        self._fill_square(rook)

        bishop = Bishop(Color.WHITE, self.game_images["white_bishop"], TupleN((7, 1)))
        self._fill_square(bishop)
        bishop = Bishop(Color.WHITE, self.game_images["white_bishop"], TupleN((7, 6)))
        self._fill_square(bishop)

        knight = Knight(Color.WHITE, self.game_images["white_knight"], TupleN((7, 2)))
        self._fill_square(knight)
        knight = Knight(Color.WHITE, self.game_images["white_knight"], TupleN((7, 5)))
        self._fill_square(knight)

        queen = Queen(Color.WHITE, self.game_images["white_queen"], TupleN((7, 3)))
        self._fill_square(queen)
        king = King(Color.WHITE, self.game_images["white_king"], TupleN((7, 4)))
        self._fill_square(king)

        for column in range(8):
            pawn = Pawn(
                Color.WHITE, self.game_images["white_pawn"], TupleN((6, column))
            )
            self._fill_square(pawn)

        for row in self.chess_board:
            for square in row:
                self._add_object(square)

    def _convert_square_to_screen_position(self, square: TupleN[int, int]):
        dimensions = (self.dimensions[0] / 8, self.dimensions[1] / 8)
        coords = (
            self.coords[0] + square[1] * dimensions[0],
            self.coords[1] + square[0] * dimensions[1],
        )

        return (coords, dimensions)

    def _fill_square(
        self, object: ChessBoardObject, square: TupleN[int, int] | None = None
    ):
        square = square if square != None else object.square
        empty_square = self.chess_board[square[0]][square[1]]
        object.coords = empty_square.coords
        object.dimensions = empty_square.dimensions
        object.pos = empty_square.pos
        self.chess_board[square[0]][square[1]] = object

    def add_empty_square(self, square: TupleN[int, int]):
        screen_pos = self._convert_square_to_screen_position(square)
        object = EmptySquare(screen_pos[0], screen_pos[1], square)
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
        return self.selected_piece

    def select_piece(self, piece: ChessBoardObject):
        self.deselect_piece()
        if piece.is_empty():
            return

        self.selected_piece = piece
        self.highlight_potential_moves()

    def highlight_potential_moves(self, piece: ChessBoardObject | None = None):
        if piece == None:
            piece = self.selected_piece
        if piece.is_empty():
            raise Exception("Empty square passed as argument")

        square = piece.square
        valid_moves = [move for move in self.possible_moves if move.start == square]
        for move in valid_moves:
            piece = self.get_piece(move.end)
            if piece.is_empty():
                self.add_valid_move_object(move.end)
            else:
                self.add_valid_take_object(move.end)

    def add_valid_move_object(self, square: tuple[int, int]):
        screen_position = self._convert_square_to_screen_position(square)
        move = ValidMove(
            screen_position[0],
            screen_position[1],
            self.game_images["valid_move"],
            screen_position[0],
            square,
        )
        self.objects.append(move)
        self._add_object(move)

    def add_valid_take_object(self, square: tuple[int, int]):
        screen_position = self._convert_square_to_screen_position(square)
        take = ValidTake(
            self,
            screen_position[0],
            screen_position[1],
            self.game_images["valid_take"],
            screen_position[0],
        )
        self.objects.append(take)
        self._add_object(take)

    def deselect_piece(self):
        self.selected_piece = None
        self.unhighlight_potential_moves()

    def unhighlight_potential_moves(self):
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
        self.possible_moves = []
        if color == None:
            color = self.color_to_move

        for row in self.chess_board:
            for piece in row:
                if not piece.is_empty() and piece.color == color:
                    self.possible_moves.extend(piece.get_moves(self.chess_board))

    def play_move(self, move: Move):
        if move not in self.possible_moves:
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
        start_piece.move(move.start, end_square.pos)
        self.chess_board[move.end[0]][move.end[1]] = start_piece
        end_square.move(move.start, start_piece.pos)
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
        coords: tuple[int, int],
        dimensions: tuple[int, int],
        square: TupleN[int, int],
        depth: int = -9,
    ):
        super().__init__(
            coords=coords,
            dimensions=dimensions,
            depth=depth,
            square=square,
            pos=coords,
        )

    def handle_left_button_down(self):
        """deselect piece"""


class ValidMove(ChessBoardObject):
    def __init__(
        self,
        coords: tuple[int, int],
        dimensions: tuple[int, int],
        image: pygame.surface,
        pos: tuple[int, int],
        square: TupleN[int, int],
        depth: int = 1,
    ):
        super().__init__(
            square=square,
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
        coords: tuple[int, int],
        dimensions: tuple[int, int],
        image: pygame.surface,
        pos: tuple[int, int],
        square: TupleN[int, int],
        depth: int = 1,
    ):
        super().__init__(
            coords=coords,
            dimensions=dimensions,
            depth=depth,
            pos=pos,
            image=image,
            square=square,
        )

    def handle_left_button_down(self):
        """'take"""

    def handle_left_button_up(self):
        """'take"""
