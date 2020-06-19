class House():
    def __init__(self, uid, location, output):
        self.id = uid
        self.location = location
        self.output = output
        
    def __repr__(self):
        return f"<HOUSE id: {self.id}, location: {self.location}>"