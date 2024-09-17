from chess.squares import Square, Orientation
from chess.moves import Move
from typing import Callable
class Piece:
    pass

# stuff to add, to implement this stuff we need to pass some other context into the functions
#
# Thes three can be solved if we pass the whole move history of the match
# We can extend the chess board to be game_context - a tuple of board and move history
# castling - the whole move history of the king and rook
# en passant - move history(at least the last move of the opponent)
# 
# Maybe don't fix this one here?
# remove king moves that end in game loss - all possible move of opposing pieces


def line_attack(square: Square, board: dict[Square: Piece], direction: Callable[[Square],Square]):
    moves = []
    piece = board[square]
    sq = direction(square)
    while sq != Square.UNKNOWN and (board[sq] == None or board[sq].color != piece.color):
        changes = {square: None, sq: piece}
        if board[sq] == None:
            moves.append(Move(changes,[]))
        else:
            moves.append(Move(changes,[board[sq]]))
        sq = direction(sq)
    return moves


def one_step_only_take(square: Square, board: dict[Square: Piece], direction: Callable[[Square],Square]):
    moves = []
    piece = board[square]
    sq = direction(square)
    if sq != Square.UNKNOWN and board[sq].color != piece.color:
        changes = {square: None, sq: piece}
        moves.append(Move(changes,[board[sq]]))
    return moves

def one_step_only_move(square: Square, board: dict[Square: Piece], direction: Callable[[Square],Square]):
    moves = []
    piece = board[square]
    sq = direction(square)
    if sq != Square.UNKNOWN and board[sq] == None:
        changes = {square: None, sq: piece}
        moves.append(Move(changes,[]))
    return moves

def one_step_attack(square: Square, board: dict[Square: Piece], direction: Callable[[Square],Square]):
    moves = []
    moves.extend(one_step_only_move(square, board, direction))
    moves.extend(one_step_only_take(square, board, direction))
    return moves

def has_moved_before(piece: Piece, prev_moves: list[Move]):
    for move in prev_moves:
        if piece in move.changes.values():
            return True
            
    return False

def last_move_long_pawn_move(prev_moves: list[Move]):
    move_count = len(prev_moves) 
    if move_count == 0:
        return False
    move = prev_moves[move_count-1]
    return hasattr(move, 'long_pawn_move') # TODO: maybe change this

def pawn_move_logic(square: Square, board: dict[Square: Piece], prev_moves: list[Move], orientaion: Orientation):
    moves = []
    pawn = board[square]

    moves.extend(one_step_only_move(square, board, orientaion.up))
    if len(moves) != 0 and not has_moved_before(pawn, prev_moves):
        moves.extend(one_step_only_move(square, board, orientaion.up(orientaion.up)))
        if len(moves) == 2:
            moves[1].long_pawn_move = True

    moves.extend(one_step_only_take(square, board, orientaion.upleft))
    moves.extend(one_step_only_take(square, board, orientaion.upright))

    if last_move_long_pawn_move(prev_moves):
        last_move = prev_moves[len(prev_moves)-1]
        #TODO: implement en passant
    return moves 

def rook_move_logic(square: Square, board: dict[Square: Piece], prev_moves: list[Move], orientaion: Orientation):
    moves = []
    moves.extend(line_attack(square, board, orientaion.up))
    moves.extend(line_attack(square, board, orientaion.down))
    moves.extend(line_attack(square, board, orientaion.left))
    moves.extend(line_attack(square, board, orientaion.right))
    
    return moves

def bishop_move_logic(square: Square, board: dict[Square: Piece], prev_moves: list[Move], orientaion: Orientation):
    moves = []
    moves.extend(line_attack(square, board, orientaion.upleft))
    moves.extend(line_attack(square, board, orientaion.upright))
    moves.extend(line_attack(square, board, orientaion.downleft))
    moves.extend(line_attack(square, board, orientaion.downright))
    
    return moves

def king_move_logic(square: Square, board: dict[Square: Piece], prev_moves: list[Move], orientaion: Orientation):
    moves = []
    
    moves.extend(one_step_attack(square, board, orientaion.up))
    moves.extend(one_step_attack(square, board, orientaion.down))
    moves.extend(one_step_attack(square, board, orientaion.left))
    moves.extend(one_step_attack(square, board, orientaion.right))
    moves.extend(one_step_attack(square, board, orientaion.upleft))
    moves.extend(one_step_attack(square, board, orientaion.upright))
    moves.extend(one_step_attack(square, board, orientaion.downleft))
    moves.extend(one_step_attack(square, board, orientaion.downright))

    return moves


def knight_move_logic(square: Square, board: dict[Square: Piece], prev_moves: list[Move], orientaion: Orientation):
    moves = []
    
    knight_move_uur = lambda sq : orientaion.up(orientaion.up(orientaion.right(sq))) 
    knight_move_uul = lambda sq : orientaion.up(orientaion.up(orientaion.left(sq))) 
    knight_move_llu = lambda sq : orientaion.left(orientaion.left(orientaion.up(sq))) 
    knight_move_lld = lambda sq : orientaion.left(orientaion.left(orientaion.down(sq))) 
    knight_move_ddl = lambda sq : orientaion.down(orientaion.down(orientaion.left(sq))) 
    knight_move_ddr = lambda sq : orientaion.down(orientaion.down(orientaion.right(sq))) 
    knight_move_rrd = lambda sq : orientaion.right(orientaion.right(orientaion.down(sq))) 
    knight_move_rru = lambda sq : orientaion.right(orientaion.right(orientaion.up(sq))) 

    moves.extend(one_step_attack(square, board, knight_move_uur))
    moves.extend(one_step_attack(square, board, knight_move_uul))
    moves.extend(one_step_attack(square, board, knight_move_llu))
    moves.extend(one_step_attack(square, board, knight_move_lld))
    moves.extend(one_step_attack(square, board, knight_move_ddl))
    moves.extend(one_step_attack(square, board, knight_move_ddr))
    moves.extend(one_step_attack(square, board, knight_move_rrd))
    moves.extend(one_step_attack(square, board, knight_move_rru))

    return moves


def queen_move_logic(square: Square, board: dict[Square: Piece], prev_moves: list[Move], orientaion: Orientation):
    moves = []
    
    moves.extend(line_attack(square, board, orientaion.up))
    moves.extend(line_attack(square, board, orientaion.down))
    moves.extend(line_attack(square, board, orientaion.left))
    moves.extend(line_attack(square, board, orientaion.right))
    moves.extend(line_attack(square, board, orientaion.upleft))
    moves.extend(line_attack(square, board, orientaion.upright))
    moves.extend(line_attack(square, board, orientaion.downleft))
    moves.extend(line_attack(square, board, orientaion.downright))

    return moves
