from chess.squares import Square


class Piece:
    pass


class Move:
    def __init__(
        self,
        changes: dict[Square:Piece],
        taken: list[Piece],
        piece: Piece,
        end_square: Square,
    ):
        self.changes = changes
        self.taken = taken
        self.piece = piece
        self._end_square = end_square

    def __eq__(self, other):
        if isinstance(other, Move):
            return (
                self.changes == other.changes
                and self.taken == other.taken
                and self.piece == other.piece
            )
        return NotImplemented

    def __ne__(self, other):
        x = self.__eq__(other)
        if x is not NotImplemented:
            return not x
        return NotImplemented

    def get_end_square(self):
        return self._end_square

    def described_by(self, piece: Piece, end: Square) -> bool:
        return self.piece == piece and self._end_square == end
