from model.Post import Post
from model.Train import Train


class World:
    def __init__(self, posts, trains):
        self.posts = {post['idx']: Post(**post) for post in posts}
        self.trains = {train['idx']: Train(**train) for train in trains}

    def update(self, update):
        self.posts = {post['idx']: Post(**post) for post in update['post']}
        for train in update['train']:
            self.trains[train['idx']].update(**train)
