import networkx as nx
from model.Move import Move
from model.Player import Player


class Strategy:
    def __init__(self, graph: nx.Graph, posts, trains, player_data):
        self.in_progress = True
        self.graph = graph
        self.posts = posts
        self.trains = trains
        self.player = self.init_player(player_data)

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
                train.departure(self.player.home, self.get_first_neighbor(self.player.home))
                line = self.get_line(train.departure_point, train.arrival_point)
                return Move(line, 1, train.idx)
            if train.current_point != self.player.home:
                train.departure(train.current_point, self.player.home)
                line = self.get_line(train.departure_point, train.arrival_point)
                return Move(line, 1, train.idx)
            self.in_progress = False

    def get_first_neighbor(self, point):
        neighbors = list(self.graph.neighbors(point))
        return neighbors[0]

    def get_line(self, u, v):
        return self.graph.get_edge_data(u, v)['idx']

    def init_player(self, player_data):
        home_idx = player_data['home']['idx']
        trains = [train['idx'] for train in player_data['train']]
        return Player(home_idx, player_data['idx'], player_data['name'], trains)


