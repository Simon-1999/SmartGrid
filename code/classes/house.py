class House():
    """Representation of a house in a SmartGrid district. A house is defined by its ID, 
    location and energy output. 
    """
    def __init__(self, uid, location, output):
        """Parameters
        ----------
        uid : int

        location : tuple

        output : float
        """
        
        self.id = uid
        self.location = location
        self.output = output
        
    def __repr__(self):
        return f"<HOUSE id: {self.id}, location: {self.location}>"