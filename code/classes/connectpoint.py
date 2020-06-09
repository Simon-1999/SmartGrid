
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

    def update_usage(self, house):
        """
        Updates the usage of the source battery of the connectpoint
        """

        self.battery.update_usage(house)