class Post:
    def __init__(self, idx, name, product, type, armor=None, population=None):
        self.armor = armor
        self.idx = idx
        self.name = name
        self.population = population
        self.product = product
        self.type = type

    def __repr__(self):
        return self.name
