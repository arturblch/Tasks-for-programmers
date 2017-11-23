class Line:
    def __init__(self, idx, length, point):
        self.idx = idx
        self.length = length
        self.point = point

    def __repr__(self):
        return str(self.idx)
