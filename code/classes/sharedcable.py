import random

class Cable():
    def __init__(self, connectpoint, battery, house):
        self.house = house
        self.connectpoint = connectpoint
        self.battery = battery
        self.path = self.cable_path(house, connectpoint)

    def cable_path(self, house, connectpoint):

        # set current location and goal location
        current_x, current_y = house.get_location()
        goal_x, goal_y = connectpoint.get_location()

        # initialize path
        path = [(current_x, current_y)] 

        # get movement direction
        hor_dist = goal_x - current_x
        if abs(hor_dist) > 0:
            hor_move = int(hor_dist / abs(hor_dist))
        ver_dist = goal_y - current_y    
        if abs(ver_dist) > 0:
            ver_move = int(ver_dist / abs(ver_dist))

        # initialize movements list
        movements = []

        # add horizontal movements 
        for x in range(abs(hor_dist)):
            movements.append((hor_move, 0))
        
        # add vertical movements to list
        for y in range(abs(ver_dist)):
            movements.append((0, ver_move))

        # shuffle list of movements
        random.shuffle(movements)

        # make path
        for movement in movements:

            # extract movement
            move_x, move_y = movement

            # increment current position
            current_x += move_x
            current_y += move_y

            # add position to path
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

    def get_path(self):
        """
        Returns cable path
        """
        return self.path
    
    def get_battery(self):
        """
        Returns the source battery
        """

        return self.battery
