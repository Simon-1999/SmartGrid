class Cable():
    def __init__(self, battery, house):
        self.house = house
        self.battery = battery
        self.path = self.cable_path(house, battery)

    def cable_path(self, house, battery):
        """ 
        Makes path of cable
        """  

        # unpack the locations
        current_x, current_y = house.location
        goal_x, goal_y = battery.location

        # create path
        path = [(current_x, current_y)]

        # make horizontal path 
        while current_x < goal_x:
            current_x += 1
            path.append((current_x, current_y))

        while current_x > goal_x:
            current_x -= 1
            path.append((current_x, current_y))

        # make vertical path
        while current_y < goal_y:
            current_y += 1
            path.append((current_x, current_y))
 
        while current_y > goal_y:
            current_y -= 1
            path.append((current_x, current_y))

        return path    

    def calc_length(self):
        """ 
        Returns length of cable 
        """  

        return len(self.path) - 1

    def calc_cost(self):
        """
        Returns the cost of the pathway
        """

        return 9 * self.calc_length()
