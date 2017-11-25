import sys
from time import sleep
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
            start_data = self.remote_process_client.login(self.name)
            map_graph = self.remote_process_client.read_map()

            strategy = Strategy(start_data[1])

            for _ in range(30):                                 # 30 ticks
                world = self.remote_process_client.read_world()

                next_move = strategy.move(world, map_graph)
                if next_move:
                    self.remote_process_client.move(next_move)
                self.remote_process_client.turn()

            self.remote_process_client.logout()
        finally:
            self.remote_process_client.close()


if __name__ == '__main__':
    Runner().run()
