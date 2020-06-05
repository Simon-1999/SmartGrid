BATTERY_COST = 5000

class Battery():
    def __init__(self, uid, location, capacity):
        # attributes of battery based on data
        self.id = uid
        self.location = location
        self.capacity = capacity
        self.cost = BATTERY_COST

        # attributes to create the grid network
        self.usage = 0
        self.houses = []
        self.cables = []

    def add_house(self, house):
        # add house to battery
        self.houses.append(house)

    def get_location(self):
        # get location of battery
        return self.location

    def update_usage(self, house):
        """
        Updates the usage of the battery
        """

        output = house.get_output()
        self.usage += output

    def reset_usage(self):
        """
        resets the batteries usage
        """

        self.usage = 0

    def is_overload(self):
        """
        Returns whether usage is still allowed within the battery's 
        capacity.
        """
        return self.capacity < self.usage

    def add_cable(self, cable_path):
        # CONCEPT
        self.cables.append(cable_path)

    def __repr__(self):
        return f"Id: {self.id} Location: {self.location}"
        

    



    