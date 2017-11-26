from model.Objects import Objects
from model.Map import Map
import networkx as nx
from model.Move import Move


class MyStrategy:
    def __init__(self, start_data):
        self.home = start_data["home"]["post_id"]
        self.ready_list = []
        self.in_progress = True

    def get_moves(self, posts, trains):
        self.posts = posts
        self.trains = trains
        moves = []
        for train_idx in self.player.trains:
            train = trains[train_idx]
            move = self.get_move(train)
            if move:
                moves.append(move)
        return moves

    # Hardcoded strategy
    def get_move(self, train):
        if train.speed == 0:
            train.arrival()
            if train.position is None:
                train.departure(self.home, self.get_first_neighbor(self.home))
                line = self.get_line(train.departure_point, train.arrival_point)
                return Move(line, 1, train.idx)
            if train.current_point != self.home:
                train.departure(train.current_point, self.home)
                line = self.get_line(train.departure_point, train.arrival_point)
                return Move(line, 1, train.idx)
            self.in_progress = False

    def get_first_neighbor(self, point):
        neighbors = list(self.graph.neighbors(point))
        return neighbors[0]

    def get_line(self, u, v):
        return self.graph.get_edge_data(u, v)['idx']
