from tuple_n import TupleN


class Move:
    def __init__(self, start: TupleN[int, int], end: TupleN[int, int]):
        self.start = start
        self.end = start
