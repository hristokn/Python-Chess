from chess.squares import Square
class Piece:
    pass

class Move:
    def __init__(self, changes: dict[Square: Piece], taken: list[Piece], piece: Piece):
        self.changes = changes
        self.taken = taken
        self.piece = piece
    
    def __eq__(self, other):
        if isinstance(other, Move):
            return (self.changes == other.changes
                    and self.taken == other.taken
                    and self.piece == other.piece)
        return NotImplemented

    def __ne__(self, other):
        x = self.__eq__(other)
        if x is not NotImplemented:
            return not x
        return NotImplemented
    
    def get_end_square(self):
        for sq, piece in self.changes.items():
            if piece == self.piece:
                return sq 
    
                
    def described_by(self, piece: Piece, end: Square) -> bool:
        try:
            correct_end = self.changes[end] == piece
        except KeyError:
            return False
        return self.piece == piece and correct_end