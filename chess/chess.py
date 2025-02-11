from chess.pieces import Piece
from chess.enums import Color, PieceType
from chess.squares import Square, WhiteOrientation
from chess.moves import Move
from collections.abc import Callable
from enum import Enum


def standard_board(board: dict[Square, None | Piece]):
    sq = Square.A2
    for _ in range(8):
        board[sq] = Piece(Color.WHITE, PieceType.PAWN)
        sq = WhiteOrientation.right(sq)

    board[Square.A1] = Piece(Color.WHITE, PieceType.ROOK)
    board[Square.B1] = Piece(Color.WHITE, PieceType.KNIGHT)
    board[Square.C1] = Piece(Color.WHITE, PieceType.BISHOP)
    board[Square.D1] = Piece(Color.WHITE, PieceType.QUEEN)
    board[Square.E1] = Piece(Color.WHITE, PieceType.KING)
    board[Square.F1] = Piece(Color.WHITE, PieceType.BISHOP)
    board[Square.G1] = Piece(Color.WHITE, PieceType.KNIGHT)
    board[Square.H1] = Piece(Color.WHITE, PieceType.ROOK)

    sq = Square.A7
    for _ in range(8):
        board[sq] = Piece(Color.BLACK, PieceType.PAWN)
        sq = WhiteOrientation.right(sq)

    board[Square.A8] = Piece(Color.BLACK, PieceType.ROOK)
    board[Square.B8] = Piece(Color.BLACK, PieceType.KNIGHT)
    board[Square.C8] = Piece(Color.BLACK, PieceType.BISHOP)
    board[Square.D8] = Piece(Color.BLACK, PieceType.QUEEN)
    board[Square.E8] = Piece(Color.BLACK, PieceType.KING)
    board[Square.F8] = Piece(Color.BLACK, PieceType.BISHOP)
    board[Square.G8] = Piece(Color.BLACK, PieceType.KNIGHT)
    board[Square.H8] = Piece(Color.BLACK, PieceType.ROOK)

class ChessBoard:
    def __init__(self, first_color: Color, board_setup: Callable[[dict[Square, None|Piece]], None] = standard_board):
        self.board = {Square(square):None for square in range(64)}
        board_setup(self.board)
        self.board_starting_state = self.board.copy()
        self.past_moves: list[Move] = []
        self.possible_moves: list[Move] = []
        self.taken_pieces: list[Piece] = []
        self.color_to_play = first_color

    def king_in_check(self, color: Color):
        other_colors = list(Color)
        other_colors.remove(color)
        for color in other_colors:
            possible_moves = self.get_possible_moves_without_king(color)
            for move in possible_moves:
                is_king = lambda piece: piece.type == PieceType.KING and piece.color == color
                if len(list(filter(is_king, move.taken))) != 0:
                    return True
        return False

    def in_checkmate(self):
        return len(self.possible_moves) == 0 and self.king_in_check(self.color_to_play)

    def in_draw(self):
        return len(self.possible_moves) == 0 and not self.in_checkmate()

    def get_possible_moves_without_king(self, color: Color) -> list[Move]:
        possible_moves = []
        for sq, piece in self.board.items():
            if piece != None and piece.color == color and piece.type != PieceType.KING:
                possible_moves.extend(piece.get_moves(sq, self.past_moves, self.board))

        possible_moves = [move for move in possible_moves if self.is_safe_move(move)]
        return possible_moves

    def get_possible_moves(self, color: Color) -> list[Move]:
        possible_moves = self.get_possible_moves_without_king(color)
        king_moves = [piece.get_moves(square, self.past_moves, self.board) for square, piece in self.board.items() if piece != None and piece.color == color and piece.type == PieceType.KING]
        for king_move in king_moves:
            king_move = [move for move in king_move if self.is_safe_move(move)]
            possible_moves.extend(king_move)
        if self.king_in_check(color):
            possible_moves = [move for move in possible_moves if not (hasattr(move, 'is_castle') and move.is_castle)]
        return possible_moves
    
    
    def update_possible_moves(self, color: Color) -> None:
        self.possible_moves = self.get_possible_moves(color)

    def is_safe_move(self, move):
        past_moves = self.past_moves.copy()
        past_moves.append(move)
        new_board = self.board.copy()
        for sq, piece in move.changes.items():
            new_board[sq] = piece

        color = self.color_to_play.next()
        possible_moves = []
        for sq, piece in new_board.items():
            if piece != None and piece.color == color:
                possible_moves.extend(piece.get_moves(sq, past_moves, new_board))

        for move in possible_moves:
            is_king = lambda piece: piece.type == PieceType.KING 
            if len(list(filter(is_king, move.taken))):
                return False
        return True

    def start(self):
        self.update_possible_moves(self.color_to_play)

    def find_square(self, piece: Piece) -> Square:
        for sq, p in self.board.items():
            if piece == p:
                return sq
        return Square.UNKNOWN
    
    def find_move(self, start: Piece, end: Square):
        move = None
        for m in self.possible_moves:
            if m.described_by(start, end):
                move = m
                break
        return move

    def multiple_moves_exist(self, start: Piece, end: Square):
        found_one = False
        for m in self.possible_moves:
            if found_one and m.described_by(start, end):
                return True
            elif m.described_by(start, end):
                found_one = True
        return False
    
    def play_move(self, move: Move | None):
        if move != None:
            self.past_moves.append(move)
            self.taken_pieces.extend(move.taken)
            for sq, piece in move.changes.items():
                self.board[sq] = piece
            self.prepare_turn()
            return True
        return False

    def get_promotion_move(self, start:Piece, end:Square, piece_type: PieceType):
        move = None
        for _move in self.possible_moves:
            if _move.described_by(start, end) and _move.changes[_move.get_end_square()].type == piece_type:
                move = _move
                break
        return move

    def prepare_turn(self):
        self.color_to_play = self.color_to_play.next()
        self.update_possible_moves(self.color_to_play)

    def turn(self, move: Move):
        self.play_move(move)
        self.prepare_turn()

    def undo_last_move(self):
        if len(self.past_moves) == 0:
            return
        last_move = self.past_moves.pop()
        for taken in last_move.taken:
            self.taken_pieces.remove(taken)

        board_states = [self.board_starting_state]
        board_states.extend([move.changes for move in self.past_moves])
        for changed_sq in last_move.changes.keys():
            for changes in reversed(board_states):
                if changed_sq in changes:
                    self.board[changed_sq] = changes[changed_sq]
                    break        
        
        self.color_to_play = self.color_to_play.previous()
        self.update_possible_moves(self.color_to_play)



class FinishedGameType(Enum):
    CHECKMATE = 0 
    RESIGN = 1
    DRAW_MATERIAL = 2 # not implemented
    DRAW_MOVES = 3
    TIMEOUT = 4

class FinishedGame:
    chess_board:ChessBoard
    winner:Color|None
    type:FinishedGameType
    def __init__(self, board, type, winner = None):
        self.chess_board = board
        type = type
        winner = winner
