import networkx as nx
from model.World import World
from model.Move import Move


# Hardcoded strategy
class Strategy:
    def __init__(self):
        self.in_progress = True

    # Возвращает наш ход
    def get_moves(self, world: World, graph: nx.Graph):
        if (world.trains[0].line_idx is None) or (world.trains[0].product == 15):
            return [Move(1, 1, 0), ]
        elif world.trains[0].product == 30:
            self.in_progress = False
