from model.Train  import Train
from model.Post  import Post

class Objects:
    def __init__(self, response):
        self.trains = [Train(train) for train in response['train']]
        self.posts = [Post(post) for post in response['post']]
