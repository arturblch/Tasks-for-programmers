from model.Objects import Objects
from model.Map import Map
from model.Move import Move


class Strategy:
    def __init__(self, start_data):
        self.ready_list = []
        self.home = start_data["home"]["idx"]
        self.my_idx = start_data["idx"]

    def move(self, objects: Objects, map: Map):
        for train in objects.trains:
            # в оконечной точке 10 hardcode
            if (train.position == None or  # start game
                    train.position  == 10 or  # p1 from line
                    train.position  == 0):  # p0 from line
                self.ready_list.append(train.idx)

        if len(self.ready_list):
            return Move(1, 1, self.ready_list.pop())

        # some logic

        return None
