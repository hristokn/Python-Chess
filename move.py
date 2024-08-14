from tuple_n import TupleN


class Move:
    def __init__(self, start: TupleN[int, int], end: TupleN[int, int]):
        self.start = start
        self.end = end

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __hash__(self):
        return hash((self.start, self.end))
