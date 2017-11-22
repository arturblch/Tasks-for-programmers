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



    def login(self, name):
        self.remote_process_client.write_message('LOGIN', f'{{"name" : {name}}}' )

    def logout(self, name):
        self.remote_process_client.write_message('LOGOUT')

    def move(self, line_idx, speed, train_idx):
        self.remote_process_client.write_message('MOVE', ' { \n' +
                                                        f' "line_idx": {line_idx}, \n ' +
                                                        f' "speed": {speed},       \n ' +
                                                        f' "train_idx": {train_idx}\n ' +
                                                         ' }')
    def turn(self, name):
        self.remote_process_client.write_message('TURN')

    def map(self, layer):
        self.remote_process_client.write_message('LOGIN', f'{{ "layer": {layer} }}')



    def run(self):
        try:
            self.login()
            strategy = Strategy()

            while True:

                strategy.move(player, player_context.world, game, move)

                self.move("MOVE", line_idx, speed, train_idx)
        finally:
            self.remote_process_client.close()


Runner().run()
