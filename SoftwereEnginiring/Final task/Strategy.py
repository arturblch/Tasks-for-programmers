from model.World import World
from model.Game import Game


# Hardcoded strategy
class Strategy:
    # Возвращает наш ход
    def move(self, world: World, game: Game):
        if world.trains[0].line_idx is None:                          # Вначале становимся на путь
            return ('MOVE', {"line_idx": 1, "speed": 1, "train_idx": 0})
        elif world.trains[0].speed != 0:                              # Едем до упора
            return ('TURN', )
        elif world.trains[0].product == 15:                           # Разворачиваемся при получении первого груза
            return ('MOVE', {"line_idx": 1, "speed": 1, "train_idx": 0})
