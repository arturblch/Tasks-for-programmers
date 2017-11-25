import sys
from Strategy import Strategy
from RemoteProcessClient import RemoteProcessClient
from model.StatusCode import StatusCode


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
            status, player_data = self.remote_process_client.login(self.name)
            if status == StatusCode.OKEY:
                try:
                    graph = self.remote_process_client.read_graph()
                    posts, trains = self.remote_process_client.read_world()
                    strategy = Strategy(graph, posts, trains, player_data)
                    while strategy.in_progress:
                        posts, trains = self.remote_process_client.update_world(trains)
                        moves = strategy.get_moves(posts, trains)
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
