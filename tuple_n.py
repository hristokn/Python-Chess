class TupleN(tuple):
    def __add__(self, other):
        if len(self) != len(other):
            return NotImplemented
        else:
            return TupleN(x + y for x, y in zip(self, other))

    def __sub__(self, other):
        if len(self) != len(other):
            return NotImplemented
        else:
            return TupleN(x - y for x, y in zip(self, other))

    def __mul__(self, other):
        if len(self) != len(other):
            return NotImplemented
        else:
            return TupleN(x * y for x, y in zip(self, other))
