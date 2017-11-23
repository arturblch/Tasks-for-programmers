from model.Point import Point
from model.Line import Line


class Game:
    def __init__(self, lines, points):
        self.points = {point['idx']: Point(**point) for point in points}
        self.lines = {line['idx']: Line(**line) for line in lines}

