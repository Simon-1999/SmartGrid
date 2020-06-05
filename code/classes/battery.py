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

    def add_house(self, house_id):
        # add house to battery
        self.houses.append(house_id)

    def get_location(self):
        # get location of battery
        return self.location

    def check_capacity(self):
        """
        Returns whether usage is still allowed within the battery's 
        capacity.
        """
        return self.capacity >= self.usage

    def add_cable(self, cable_path):
        # CONCEPT
        self.cables.append(cable_path)

    def __repr__(self):
        return f"Id: {self.id} Location: {self.location}"
        

    



    