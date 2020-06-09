class House():
    def __init__(self, uid, location, output):
        self.id = uid
        self.location = location
        self.output = output
        self.cable = None

    def get_location(self):
        """ Returns location """
    
        return self.location

    def get_output(self):
        """ 
        Get the output energy of a house
        """

        return self.output

    def add_cable(self, cable):
        """
        Adds a cable object
        """
        self.cable = cable

    def has_cable(self):
        """
        Checks if house has a cable
        """
        
        return self.cable is not None
        
    def __repr__(self):
        return f"Id: {self.id} Location: {self.location}"