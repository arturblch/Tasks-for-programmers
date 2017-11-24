import networkx as nx
import pygame as pg
from Runner import Runner
from Strategy import Strategy

BACKGROUND_IMAGE = 'grass.jpg'

class GUI:
    def __init__(self, width=600, height=600):
        pg.init()
        self.width = width
        self.height = height
        self.screen = pg.display.set_mode((self.width,self.height ))
        self.background = pg.image.load(BACKGROUND_IMAGE).convert_alpha()
        self.G = None
        self.clock = pg.time.Clock()
        self.fps = 60
        pg.display.set_caption("Train Game")
        self.myfont = pg.font.SysFont('arial', 15)

    def bild_net(self, game_responce):
        Graph = nx.Graph()
        Graph.add_nodes_from([(point.pop('idx'),point) for point in game_responce["point"]])
        Graph.add_edges_from([line.pop('point')+[line,] for line in game_responce["line"]])

        return Graph

    def _draw_point(self, colour):
        pass

    def run(self):
        client = Runner()
        done = False
        try:
            start_data = self.remote_process_client.login(self.name)
            while not done:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        done = True

                pg.display.flip()
                self.clock.tick(self.fps)
        pg.quit()

if __name__ == '__main__':
    gui = GUI()
    gui.run()
