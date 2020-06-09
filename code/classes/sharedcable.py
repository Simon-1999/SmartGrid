class SharedCable():
    def __init__(self, battery):
        self.houses = [] # list must be order from closest to farest house
        self.battery = battery
        self.fixedpoints = []
        self.path = []

    def calc_cable_path(self):
        """ 
        Calculate path of cable 
        """

        # reset path and fixedpoints
        self.path = []
        self.fixedpoints = [self.battery.get_location()]

        # add branch for every house
        for house in self.houses:

            current_location = house.get_location()
            goal_location = self.nearest_fixedpoint(current_location)
            self.add_branch(current_location, goal_location)      

    def add_branch(self, current_location, goal_location):
        """ 
        Calculate path from current to goal location 
        """

        # set current location and goal location
        current_x, current_y = current_location
        goal_x, goal_y = self.nearest_fixedpoint(current_location)

        # loop through path horizontally and vertically respectively
        while current_x < goal_x:
            current_x += 1
            if (current_x, current_y) not in self.path:
                self.path.append((current_x, current_y)) 

        while current_x > goal_x:
            current_x -= 1
            if (current_x, current_y) not in self.path:
                self.path.append((current_x, current_y)) 

        while current_y < goal_y:
            current_y += 1
            if (current_x, current_y) not in self.path:
                self.path.append((current_x, current_y)) 
 
        while current_y > goal_y:
            current_y -= 1
            if (current_x, current_y) not in self.path:
                self.path.append((current_x, current_y)) 

        self.fixedpoints.append(current_location)

    def nearest_fixedpoint(self, current_location):
        """ 
        Find nearest fixedpoint 
        """

        current_x, current_y = current_location
        min_dist = 100

        # loop through all fixed points
        for fixedpoint in self.fixedpoints:

            fixedpoint_x, fixedpoint_y = fixedpoint
            dist = abs(current_x - fixedpoint_x) + abs(current_y - fixedpoint_y)
            
            # overwrite minimum distance and save that fixedpoint
            if dist < min_dist:

                min_dist = dist
                nearest_fixedpoint = fixedpoint

        return nearest_fixedpoint

    def calc_length(self):
        """ 
        Returns length of cable 
        """ 

        return len(self.path) - 1

    def get_cost(self):
        """
        Returns the cost of the pathway
        """

        return self.calc_length() * 9

    def add_house(self, house):
        """
        Adds house to cable and calculates new cable path
        """

        self.houses.append(house)

        def dist_battery(house):
            """
            Returns distance from battery
            """

            house_x, house_y = house.get_location()
            battery_x, battery_y = self.battery.get_location()

            return abs(house_x - battery_x) + abs(house_y - battery_y)

        # make sure list of houses is order from closest to farest to battery
        self.houses.sort(key=dist_battery)

        # recalculate path
        self.calc_cable_path()

    