class Battery():
    def __init__(self, uid, location, capacity, cost):
        # attributes of battery based on data
        self.id = uid
        self.location = location
        self.capacity = capacity
        self.cost = cost

        # attributes to create the grid network
        self.usage = 0
        self.houses = []
        self.cables = []

    def add_house(self, house):
        """ 
        Add house to battery and updates usage
        """ 

        self.houses.append(house)
        self.update_usage(house)

    def add_cable(self, cable):
        """
        Adds a cable object
        """

        self.cables.append(cable)

    def get_location(self):
        """
        Get location of battery
        """

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


    def calc_overload(self, house):
        """
        Calculates if a battery gets overloaded by adding an house object.
        """
        # get output of the house
        output = house.get_output()

        # check if the battery capacity is exceeded by adding a house
        if (output + self.usage) > self.capacity:
            return True

        return False


    def get_cost(self):
        """
        Returns the cost of the battery
        """
        return self.cost


    def __repr__(self):
        return f"Id: {self.id} Location: {self.location} Usage: {self.usage}"
        

    



    