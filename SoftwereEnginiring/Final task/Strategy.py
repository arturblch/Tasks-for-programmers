import networkx as nx
from model.World import World
from model.Move import Move
from model.Player import Player


# Hardcoded strategy
class Strategy:
    def __init__(self, graph: nx.Graph, world: World, player_data):
        self.in_progress = True
        self.graph = graph
        self.world = world
        self.player = self.init_player(player_data, graph, world)

    # Возвращает наш ход
    def get_moves(self, world: World):
        self.world = world

        # if (world.trains[0].line_idx is None) or (world.trains[0].product == 15):
        #     return [Move(1, 1, 0), ]
        # elif world.trains[0].product == 30:
        #     self.in_progress = False
        moves = []
        for train_idx in self.player.trains:
            train = world.trains[train_idx]
            move = self.get_move(train)
            if move:
                moves.append(move)
        return moves

        # print(list(graph.neighbors(self.player.home_idx)))

    def get_move(self, train):
        print('cda', train.current_point, train.departure_point, train.arrival_point)
        if train.speed == 0:
            train.arrival()
            if train.position is None:
                train.departure(self.player.home, self.get_first_neighbor(self.player.home))
                line = self.get_line(train.departure_point, train.arrival_point)
                return Move(line, 1, train.idx)
            # print('cda', train.current_point, train.departure_point, train.arrival_point)
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

    def init_player(self, player_data, graph, world):
        home_idx = player_data['home']['idx']
        trains = [train['idx'] for train in player_data['train']]
        return Player(home_idx, player_data['idx'], player_data['name'], trains)


