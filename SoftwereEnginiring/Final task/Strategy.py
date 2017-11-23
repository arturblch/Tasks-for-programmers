from model.World import World
from model.Game import Game
from model.Move import Move


class Strategy:
    def __init__(self, start_data):
        self.ready_list = []
        self.home = start_data["home"]["idx"]

    def move(self, world: World, game: Game):
        for train in world.trains:
            # в оконечной точке 10 hardcode
            if (train["position"] == None or  # start game
                    train["position"] == 10 or  # p1 from line
                    train["position"] == 0):  # p0 from line
                self.ready_list.append(train["idx"])

        if len(self.ready_list):
            train = None
            while len(self.ready_list):
                train = self._get_train(self.ready_list.pop(), world)
                if not train:
                    continue

            if train:
                next_line = self.get_next_line(train, game)
                return Move(
                    line_idx=next_line, speed=1, train_idx=train["idx"])

        # some logic

        return None

    def get_next_line(self, train, game):
        line = self._get_line(train["line_idx"], game)

        if line == None:
            point = self.home
        else:
            # Хитрое упрощение, логическая переменная подставляеться как индекс списка
            point = line["point"][train["position"] == line["length"]]

        possible_lines = self._find_lines_at_point(point, game)
        if possible_lines:
            return possible_lines[-1]

    def _find_lines_at_point(self, point_idx, game):
        lines = []
        for line in game.lines:
            if point_idx in line["point"]:
                lines.append(line["idx"])
        return lines

    def _get_line(self, line_idx, game):
        for line in game.lines:
            if line["idx"] == line_idx:
                return line

        return None

    def _get_train(self, train_idx, world):
        for train in world.trains:
            if train["idx"] == train_idx:
                return train

        return None
