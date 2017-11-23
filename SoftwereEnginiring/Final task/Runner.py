import sys
from time import sleep

# from Strategy import Strategy
from RemoteProcessClient import RemoteProcessClient


class Runner:
    def __init__(self):
        if sys.argv.__len__() == 4:
            self.remote_process_client = RemoteProcessClient(sys.argv[1], int(sys.argv[2]))
            self.name = sys.argv[3]
        else:
            self.remote_process_client = RemoteProcessClient('wgforge-srv.wargaming.net', 443)
            self.name = "Mickey"

    def login(self, name):
        return self.remote_process_client.write_message('LOGIN', {"name": name})

    def logout(self):
        return self.remote_process_client.write_message('LOGOUT')

    def move(self, line_idx, speed, train_idx):
        return self.remote_process_client.write_message('MOVE', {"line_idx": line_idx, "speed": speed, "train_idx": train_idx})

    def turn(self):
        return self.remote_process_client.write_message('TURN')

    def map(self, layer):
        return self.remote_process_client.write_message('MAP', {"layer": layer})

    def run(self):
        try:
            self.login(self.name)
            # strategy = Strategy()
            self.move(1, 1, 0)
            for i in range(10):
                # world = self.remote_process_client.read_world()
                self.turn()
                data = self.map(1)
                print("Position - ", data[1]["train"][0]["position"])

                # move = Move()
                # strategy.move(world, game, move)

            self.logout()
        finally:
            self.remote_process_client.close()


if __name__ == '__main__':
    Runner().run()
