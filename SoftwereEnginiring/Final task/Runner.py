import sys

#from Strategy import Strategy
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
        self.remote_process_client.write_message('LOGIN', {"name" : name})
        

    def logout(self):
        self.remote_process_client.write_message('LOGOUT')

    def move(self, line_idx, speed, train_idx):
        self.remote_process_client.write_message('MOVE', {"line_idx": line_idx, "speed": speed, "train_idx": train_idx})
    def turn(self):
        self.remote_process_client.write_message('TURN')

    def map(self, layer):
        self.remote_process_client.write_message('MAP', {"layer": layer })
        return self.remote_process_client.read_response()


    def run(self):
        try:
            self.login(self.name)
            strategy = Strategy()

            while True:

                strategy.move(player, player_context.world, game, move)

                self.move("MOVE", line_idx, speed, train_idx)
        finally:
            self.remote_process_client.close()


if __name__ == '__main__':
    Runner().run()
