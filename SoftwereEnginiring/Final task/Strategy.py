from model.World import World
from model.Game import Game
from model.Move import Move


class MyStrategy:
    def __init__(self, start_data):
        self.home_post = start_data["home"]["post_id"]
        self.ready_list = []

    def move(self, world: World, game: Game):
        for train in world.trains
        # в оконечной точке 10 hardcode
            if (train["position"] == None or    # start game
                train["position"] == 10 or      # p1 from line
                train["position"] == 0):        # p0 from line
                self.ready_list.append(world.train["idx"])

        if len(ready_list):
            train = None
            while len(ready_list):
                train = self._get_train(ready_list.pop())
                if not train:
                    continue

            if train:
                next_line = self.get_next_line(train)
                return Move(line_idx=next_line,
                            speed=1,
                            train_idx=train["idx"])

        # some logic

        return None

    def get_next_line(self, train):
        line = self._get_line(self, train["line_idx"]):
            # Хитрое упрощение, логическая переменная подставляеться как индекс списка
        point = line["point"][train["position"] == line["length"]]

        possible_lines = self._find_lines_at_point(point)
        if possible_lines:
            return possible_lines[0]

    def _find_lines_at_point(self, point_idx):
        lines = []
        for line in game.lines:
            if point_idx in line["point"]:
                lines.append(line["idx"])
        return lines

    def _get_line(self, line_idx):
        for line in game.lines:
            if line["idx"] == line_idx:
                return train

        return None

    def _get_train(self, train_idx):
        for train in world.trains:
            if train["idx"] == train_idx:
                return train

        return None
