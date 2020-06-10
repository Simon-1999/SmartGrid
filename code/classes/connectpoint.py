
class Connectpoint():
    def __init__(self, location, battery):
        self.location = location
        self.battery = battery

    def get_location(self):
        """
        Returns the location of the connectpoint
        """

        return self.location

    def get_battery(self):
        """
        Get source battery of the connectpoint
        """

        return self.battery

    def __repr__(self):
        return f"Connectpoint location: {self.location} battery: {self.battery}"