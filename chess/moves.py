from chess.squares import Square
class Piece:
    pass

class Move:
    def __init__(self, changes: dict[Square: Piece], taken: list[Piece], piece: Piece):
        self.changes = changes
        self.taken = taken
        self.piece = piece
    
    def __str__(self) -> str:
        if len(self.changes) != 2 or len(self.taken) > 1:
            raise NotImplementedError
        
        result = ''
        starting_square = Square.UNKNOWN
        end_square = Square.UNKNOWN
        piece = None
        if len(self.taken):
            result = result + 'x'
        for sq, _piece in self.changes.items():
            if _piece == None:
                starting_square = sq                
            elif _piece != None:
                end_square = sq
                piece = _piece

        if piece.type.value == 0: #not cool, fix this TODO
            result = result + str(end_square)
        else:
            result = str(piece) + str(starting_square) + result + str(end_square)
        return result   
            
