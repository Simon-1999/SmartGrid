class Battery():
    def __init__(self, uid, location, capacity, cost):
        self.id = uid
        self.location = location
        self.capacity = capacity
        self.cost = cost

    def __repr__(self):
        return f"<BATTERY id: {self.id}, location: {self.location}>"
    