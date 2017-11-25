import sys
from Strategy import Strategy
from RemoteProcessClient import RemoteProcessClient


class Runner:
    def __init__(self):
        if sys.argv.__len__() == 4:
            self.remote_process_client = RemoteProcessClient(sys.argv[1], int(sys.argv[2]))
            self.name = sys.argv[3]
        else:
            self.remote_process_client = RemoteProcessClient('wgforge-srv.wargaming.net', 443)
            self.name = "Mickey"

    def run(self):
        try:
            self.remote_process_client.login(self.name)
            try:
                graph = self.remote_process_client.read_graph()
                strategy = Strategy()
                while strategy.in_progress:
                    world = self.remote_process_client.read_world()
                    moves = strategy.get_moves(world, graph)
                    if moves:
                        for move in moves:
                            self.remote_process_client.move(move)
                    self.remote_process_client.turn()
            finally:
                self.remote_process_client.logout()
        finally:
            self.remote_process_client.close()


if __name__ == '__main__':
    Runner().run()
