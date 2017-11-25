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
    def get_moves(self, graph: nx.Graph, world: World):
        self.world = world
        if (world.trains[0].line_idx is None) or (world.trains[0].product == 15):
            return [Move(1, 1, 0), ]
        elif world.trains[0].product == 30:
            self.in_progress = False

    def init_player(self, player_data, graph, world):
        home = player_data['home']['idx']
        trains = [world.trains[train['idx']] for train in player_data['train']]
        return Player(graph.nodes[home], player_data['idx'], player_data['name'], trains)
