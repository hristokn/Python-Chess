from chess.squares import Square, Orientation
from chess.moves import Move
from chess.enums import PieceType
from typing import Callable
from copy import deepcopy
class Piece:
    pass

# the king needs to know if he is check. if he is, he can't castle

def line_attack(square: Square, board: dict[Square: Piece], direction: Callable[[Square],Square]):
    moves = []
    piece = board[square]
    sq = direction(square)
    while sq != Square.UNKNOWN and (board[sq] == None or board[sq].color != piece.color):
        changes = {square: None, sq: piece}
        if board[sq] == None:
            moves.append(Move(changes,[], piece, sq))
        else:
            moves.append(Move(changes,[board[sq]], piece, sq))
            break
        sq = direction(sq)
    return moves


def one_step_only_take(square: Square, board: dict[Square: Piece], direction: Callable[[Square],Square]):
    moves = []
    piece = board[square]
    sq = direction(square)
    if sq != Square.UNKNOWN and board[sq] != None and board[sq].color != piece.color:
        changes = {square: None, sq: piece}
        moves.append(Move(changes,[board[sq]], piece, sq))
    return moves

def one_step_only_move(square: Square, board: dict[Square: Piece], direction: Callable[[Square],Square]):
    moves = []
    piece = board[square]
    sq = direction(square)
    if sq != Square.UNKNOWN and board[sq] == None:
        changes = {square: None, sq: piece}
        moves.append(Move(changes,[], piece, sq))
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

def last_move_is_long_pawn_move(prev_moves: list[Move]):
    move_count = len(prev_moves) 
    if move_count == 0:
        return False
    
    move = prev_moves[move_count-1]
    piece = move.piece
    if piece.type != PieceType.PAWN:
        return False
    
    end_square = move.get_end_square()
    orientation = move.piece.orientation
    start_square = orientation.down(orientation.down(end_square))

    if move.changes == {start_square: None, move.get_end_square(): move.piece}:
        return True
    return False

def can_promote(move: Move, direction):
    if move.get_end_square() != Square.UNKNOWN and direction(move.get_end_square()) == Square.UNKNOWN:
        return True

def promote(move: Move):
    moves = []

    types_to_promote = [PieceType.BISHOP, PieceType.QUEEN, PieceType.KNIGHT, PieceType.ROOK] 
    for type in types_to_promote:
        new_piece = deepcopy(move.piece)
        new_piece.type = type
        new_changes = deepcopy(move.changes)
        new_changes[move.get_end_square()] = new_piece
        new_move = Move(new_changes, move.taken, move.piece, move.get_end_square())
        moves.append(new_move)

    return moves

def castle(square: Square, board: dict[Square: Piece], prev_moves: list[Move], direction: Callable[[Square],Square]):
    moves = []
    king = board[square]
    if has_moved_before(king, prev_moves):
        return moves

    sq1 = direction(square)
    sq2 = direction(sq1)
    sq3 = direction(sq2)
    sq4 = direction(sq3)
    rook_square = Square.UNKNOWN
    move = Move({square: None, sq2: king}, [], king, sq2)
    if sq4 != Square.UNKNOWN and board[sq1] == None and board[sq2] == None and board[sq3] == None:
        rook_square = sq4
    elif sq3 != Square.UNKNOWN and board[sq1] == None and board[sq2] == None:
        rook_square = sq3
    else:
        return moves

    rook = board[rook_square]
    if rook != None and not has_moved_before(rook, prev_moves):
        move.changes[rook_square] = None
        move.changes[sq1] = rook
        move.is_castle = True
        moves.append(move)

    return moves
    
def pawn_move_logic(square: Square, board: dict[Square: Piece], prev_moves: list[Move], orientaion: Orientation):
    moves = []
    pawn = board[square]

    moves.extend(one_step_only_move(square, board, orientaion.up))
    if len(moves) != 0 and not has_moved_before(pawn, prev_moves):
        two_up = lambda sq: orientaion.up(orientaion.up(sq))
        moves.extend(one_step_only_move(square, board, two_up))

    moves.extend(one_step_only_take(square, board, orientaion.upleft))
    moves.extend(one_step_only_take(square, board, orientaion.upright))

    if last_move_is_long_pawn_move(prev_moves):
        last_move = prev_moves[len(prev_moves)-1]
        last_move_end_square = last_move.get_end_square()
        if orientaion.left(square) == last_move_end_square or orientaion.right(square) == last_move_end_square:
            end_square = orientaion.up(last_move_end_square)
            move = Move({square: None, last_move_end_square: None, end_square: pawn},[last_move.piece],pawn, end_square)
            moves.append(move)

    _moves = moves.copy()
    for move in _moves:
        if can_promote(move, orientaion.up):
            moves.remove(move)
            moves.extend(promote(move))

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

    moves.extend(castle(square, board, prev_moves, orientaion.left))
    moves.extend(castle(square, board, prev_moves, orientaion.right))

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
