"""The SharedGreedy algorithm uses a configuration that has already been formed for a district, and 
places cables in a greedy manner. 
The batteries themselves are used as the first 'connectpoints', and the houses get a cable to them one by one
after being sorted on their distance from the battery. When a house's path is added, all the pathway points
are added as connectpoints, and the next house connects to the closest connectpoint. This way, all houses end 
up connected to their battery. 
"""

import copy
import random
import matplotlib.pyplot as plt
import numpy

from .algorithm import Algorithm

class SharedGreedy(Algorithm):
    """Connects houses to their battery in a greedy way. The closest house is added directly to the battery, then
    after that the next house is connected to the closest existing 'connectpoint', i.e. the closest existing cable
    or the battery itself when that's closer. 

    Methods
    ----------
    run()
        Runs the SharedGreedy algorithm

    get_nearest_connectpoint(battery, house)
        Gets nearest connectpoint for a house 

    get_cable_path(start_location, end_location)
        Creates a shortest Manhattan path between two points in a random x,y order

    init_connectpoints()
        Initializes the batteries of the district as the first connectpoints

    plot_cables(district)
        Plots the conplete district with its paths
    """

    def __init__(self, district):
        """Parameters
        ----------
        district : District object
            A district with a prior configuration
        """
        self.district = district
        self.free_houses = []
        self.iterations = 0
        self.connectpoints = self.init_connectpoints()


    def run(self):
        """Runs the SharedGreedy algorithm

        Returns
        ----------
        District object
        """

        self.district.reset_cables()

        # loop through batteries
        for battery in self.district.batteries:

            houses = self.district.connections[battery.id]

            # sort houses from on distance from battery
            houses.sort(key=lambda house: self.calc_dist(house.location, battery.location))

            # loop through houses
            for house in houses:

                # find nearest connectpoint
                connectpoint = self.get_nearest_connectpoint(battery, house)   

                # make cable path
                path = self.get_cable_path(house.location, connectpoint) 
                self.district.cables[house.id] = path

                # add path to connectpoints
                for point in path:
                    self.connectpoints[battery.id].append(point)  

        print("SharedGreedy done ")
        return self.district

    def get_nearest_connectpoint(self, battery, house):
        """Finds the nearest connectpoint for a house to connect to. 
        """

        return min(self.connectpoints[battery.id], key=lambda \
            location: self.calc_dist(location, house.location))

    def get_cable_path(self, start_location, end_location):
        """Collects necessary x- and y-movements between two locations to create a path with
        the shortest Manhattan distance. The movements are then shuffled to create a random
        order. 

        Parameters
        ----------
        start_location : tuple

        end_location : tuple

        Returns
        ----------
        list
            The formed path, a list of tuples as representation
        """

        # unpack location
        current_x, current_y = start_location
        end_x, end_y = end_location

        # initialize path
        path = [(current_x, current_y)] 

        # get movement direction
        hor_dist = end_x - current_x
        if abs(hor_dist) > 0:
            hor_move = int(hor_dist / abs(hor_dist))
        ver_dist = end_y - current_y    
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


    def init_connectpoints(self):
        """Initializes the batteries in a district as the first connectpoints. 
        """

        connectpoints = {}

        for battery in self.district.batteries:

            connectpoints[battery.id] = [battery.location]

        return connectpoints