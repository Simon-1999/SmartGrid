class Battery():
    """Representation of a battery in a SmartGrid district. A battery is defined by its ID, 
    location, capacity and building costs. 
    """

    def __init__(self, uid, location, capacity, cost):
        """Parameters
        ----------
        uid : int
        
        location : tuple

        capacity : float

        cost : float
        """
        self.id = uid
        self.location = location
        self.capacity = capacity
        self.cost = cost
        

    def __repr__(self):
        return f"<BATTERY id: {self.id}, location: {self.location}>"
    