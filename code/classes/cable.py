class Cable():
    def __init__(self, house, battery):
        self.house = house
        self.battery = battery
        self.path = self.cable_path(house, battery)

    def cable_path(self, house, battery):
        # unpack the locations into variables
        house_x, house_y = house.get_location()
        batt_x, batt_y = battery.get_location()

        # set current location and goal location
        current_x = min(house_x, batt_x) 
        goal_x = max(house_x, batt_x)
        current_y = min(house_y, batt_y)
        goal_y = max(house_y, batt_y)

        # create path
        path = [(current_x, current_y)]

        # loop through path horizontally and vertically respectively
        while current_x < goal_x:
            current_x += 1
            path.append((current_x, current_y))

        while current_y < goal_y:
            current_y += 1
            path.append((current_x, current_y))

        return path    


    def calc_length(self):
        """ Returns length of cable """  
        return len(self.path) - 1

    def get_cost(self):
        """
        Returns the cost of the pathway
        """
        length = self.calc_length()
        total = 9 * length

        return total
