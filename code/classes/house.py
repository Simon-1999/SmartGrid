class House():
    def __init__(self, uid, location, output):
        self.id = uid
        self.location = location
        self.output = output
        self.cable = None

    def get_location(self):
        """ Returns location """
    
        return self.location

    def __repr__(self):
        return f"Id: {self.id} Location: {self.location}"