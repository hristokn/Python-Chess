from chess.pieces import Piece, Move
from chess.enums import Color, PieceType
from chess.squares import Square, WhiteOrientation
from chess.moves import Move

class ChessBoard:
    def __init__(self):
        self.board = {}
        self.standard_board(self.board)
        self.past_moves = []
        self.possible_moves = []
        self.taken_pieces = []
        self.color_to_play = Color.WHITE

    def calc_possible_moves(self, color: Color):
        self.possible_moves = []
        for sq, piece in self.board.items():
            if piece != None and piece.color == color:
                self.possible_moves.extend(piece.get_moves(sq, self.past_moves, self.board))
            
    def start(self):
        self.prepare_turn()

    def play_move(self, move: Move):
        if not move in self.possible_moves:
            return False
        
        self.taken_pieces.extend(move.taken)
        for sq, piece in move.changes.items():
            self.board[sq] = piece
        return True

    def print_possible_moves(self):
        i = 1
        for move in self.possible_moves:
            print(str(i) + ' ' + str(move))
            i = i + 1

    def prepare_turn(self):
        self.calc_possible_moves(self.color_to_play)

    def turn(self, move: Move):
        self.play_move(move)
        self.next_color()
        self.prepare_turn()
        
    def next_color(self):
        if self.color_to_play == Color.WHITE:
            self.color_to_play = Color.BLACK
        elif self.color_to_play == Color.BLACK:
            self.color_to_play = Color.WHITE

    def standard_board(self, board):
        for square in range(64):
            board[Square(square)] = None
        
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
