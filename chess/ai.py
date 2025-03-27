from chess.chess import ChessBoard, Piece
from chess.enums import Color, PieceType
from chess.squares import Square
from chess.moves import Move
from random import randint
from threading import Thread
from copy import deepcopy


piece_values = {
    PieceType.PAWN: 1,
    PieceType.KNIGHT: 3,
    PieceType.BISHOP: 3,
    PieceType.ROOK: 5,
    PieceType.QUEEN: 9,
    PieceType.KING: 1000,
}



class AIMove(Thread):
    def __init__(self, chess_board, color):
        Thread.__init__(self)
        self.runnable = pick_move
        self.chess_board = chess_board
        self.move = None
        self.color = color
    def run(self):
        self.move = self.runnable(self.chess_board, self.color)


def pick_move(chess_board: ChessBoard, color: Color):

    piece_count = len([piece for piece in chess_board.board.values() if piece != None])
    maximising = color == Color.WHITE
    boardstate = Boardstate(chess_board)
    boardstate.killer_move = None
    boardstate.killer_move_depth = None
    index = len(boardstate.past_moves)
    if piece_count > 8:
        value = alphabeta_rec(boardstate, 3, _min,  _max, maximising, index)
    # else:
    #     value = alphabeta_rec(boardstate, 10, -1,  +1, maximising, index)

    return value.move



class Boardstate:
    def __init__(self, chessboard: ChessBoard):
        cb = deepcopy(chessboard)
        self.board: dict[Square, Piece] = cb.board
        self.board_starting_state: dict[Square, Piece] = cb.board_starting_state
        self.past_moves: list[Move] = cb.past_moves
        self.color_to_play: Color = cb.color_to_play
        self.moves = self.calc_possible_moves()

    def play_move(self, move: Move):
        for changed_sq, changed_piece in move.changes.items():
            self.board[changed_sq] = changed_piece
        self.past_moves.append(move)
        self.color_to_play = self.color_to_play.next()
        self.moves = self.calc_possible_moves()
        self.moves.sort(key = lambda move: sum([piece_values[taken.type] for taken in move.taken]),reverse=True)
        
    def get_possible_moves(self):
        return self.moves
    
    def calc_possible_moves(self, color: Color = ...):
        moves = []
        if color == ...:
            color = self.color_to_play
        for sq, piece in self.board.items():
            if piece != None and piece.color == color:
                moves.extend(piece.get_moves(sq, self.past_moves, self.board))
        return moves
    
    def undo_last_move(self):
        if len(self.past_moves) == 0:
            return
        last_move = self.past_moves.pop()

        board_states = [self.board_starting_state]
        board_states.extend([move.changes for move in self.past_moves])
        for changed_sq in last_move.changes.keys():
            for changes in reversed(board_states):
                if changed_sq in changes:
                    self.board[changed_sq] = changes[changed_sq]
                    break        
        
        self.color_to_play = self.color_to_play.previous()


    def value_board(self):
        MOVE_VALUE = 0.02
        CHECK_VALUE = 0.50
        TAKE_VALUE = 0.10
        white_piece_value = sum([piece_values[piece.type] for piece in self.board.values() if piece != None and piece.color == Color.WHITE])
        black_piece_value = sum([piece_values[piece.type] for piece in self.board.values() if piece != None and piece.color == Color.BLACK])
        
        white_move_value = 0
        white_take_value = 0
        black_move_value = 0
        black_take_value = 0
        if self.color_to_play == Color.WHITE:
            moves = self.get_possible_moves() 
            white_move_value = len(moves)*MOVE_VALUE
            white_take_value = len([move for move in moves if len(move.taken) != 0])*TAKE_VALUE

            moves = self.calc_possible_moves(Color.BLACK) 
            black_move_value = len(moves)*MOVE_VALUE
            black_take_value = len([move for move in moves if len(move.taken) != 0])*TAKE_VALUE
        else:
            moves = self.calc_possible_moves(Color.WHITE) 
            white_move_value = len(moves)*MOVE_VALUE
            white_take_value = len([move for move in moves if len(move.taken) != 0])*TAKE_VALUE
            
            moves = self.get_possible_moves() 
            black_move_value = len(moves)*MOVE_VALUE
            black_take_value = len([move for move in moves if len(move.taken) != 0])*TAKE_VALUE

        return white_piece_value + white_move_value + white_take_value - black_piece_value - black_move_value - black_take_value

class ValueMove:
    def __init__(self, value, move):
        self.value = value
        self.move = move

    def min(self, other):
        if other.value < self.value:
            return other
        else: 
            return self
        
    def max(self, other):
        if other.value > self.value:
            return other
        else: 
            return self
_min = ValueMove(float('-inf'), None)
_max = ValueMove(float('inf'),None)
        


def alphabeta_rec(boardstate: Boardstate, depth:int, alpha:ValueMove, beta:ValueMove, maximizingPlayer:bool, index):
    moves = boardstate.get_possible_moves()
    if depth == 0 or len(moves) == 0:
        return ValueMove(boardstate.value_board(), boardstate.past_moves[index])
    if maximizingPlayer:
        value = _min
        child = boardstate
        if boardstate.killer_move != None and moves.count(boardstate.killer_move) != 0:
            first_move = moves[0]
            killer_move_index = moves.index(boardstate.killer_move)
            moves[0] = boardstate.killer_move
            moves[killer_move_index] = first_move
        for move in moves:
            child.play_move(move)
            value = value.max(alphabeta_rec(child, depth - 1, alpha, beta, False, index))
            alpha = alpha.max(value)
            if value.value >= beta.value:
                boardstate.killer_move = move
                boardstate.killer_move_depth = depth
                child.undo_last_move()
                break 
            child.undo_last_move()
        return value
    else:
        value = _max
        child = boardstate
        for move in moves:
            child.play_move(move)
            value = value.min(alphabeta_rec(child, depth - 1, alpha, beta, True, index))
            beta = beta.min(value)
            if value.value <= alpha.value:
                child.undo_last_move()
                break 
            child.undo_last_move()
        return value