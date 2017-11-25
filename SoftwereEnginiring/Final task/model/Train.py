class Train:
    def __init__(self, capacity, idx, line_idx, player_id, position, product, speed):
        self.capacity = capacity
        self.idx = idx
        self.line_idx = line_idx
        self.player_id = player_id
        self.position = position
        self.product = product
        self.speed = speed
        self.departure_point = None
        self.arrival_point = None
        self.current_point = None

    def departure(self, departure_point, arrival_point):
        self.current_point = None
        self.departure_point = departure_point
        self.arrival_point = arrival_point

    def arrival(self):
        self.current_point = self.arrival_point
        self.arrival_point = None
        self.departure_point = None

    def update(self, capacity, idx, line_idx, player_id, position, product, speed):
        self.capacity = capacity
        self.idx = idx
        self.line_idx = line_idx
        self.player_id = player_id
        self.position = position
        self.product = product
        self.speed = speed
