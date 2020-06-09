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

    def add_house(self, house):
        # add house to battery
        self.houses.append(house)
        self.usage += house.get_output()

    def get_location(self):
        # get location of battery
        return self.location
       
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

    def get_cost(self):
        """
        Returns the cost of the battery
        """
        return self.cost

    def get_cable(self):
        """
        Returns cable object
        """

        return self.cable


    def add_cable(self, cable):
        """
        Adds cable object to attribute cable
        """

        self.cable = cable

    def __repr__(self):
        return f"Id: {self.id} Location: {self.location}"
        

    



    