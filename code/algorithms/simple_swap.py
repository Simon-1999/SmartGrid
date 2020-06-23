"""SimpleSwap repeatedly loops through the houses in a (for example randomly) configurated ditrict, starting at the house with
the longest connection, and searches for a house with similar output. If the swapping of the connections between these houses 
results in lower costs, the houses are swapped regarding their batteries. 
"""

import numpy as np
import time
import copy
from .algorithm import Algorithm

class SimpleSwap(Algorithm):
    """Optimizing a district by swapping longest cables with a better alternative. A house with a relatively long cable
    looks for a house that has similar output and where swapping would result in less costs. 

    Methods
    ----------
    run()
        Runs the algorithm.

    sort_connections()
        Sorts connections in the district based on length.

    find_swap(connection)
        Looks for a beneficial swapping option.

    swap(current_connection, swap_connection)
        Swaps two houses with respect to the batteries they're connected to. 
    """

    def __init__(self, district):
        """Parameters
        ----------
        district : District object
        """
        self.district = district
        self.iterations = 0

    
    def run(self):
        """Runs the SimpleSwap algorithm.
        """
        # sort connections based on length
        sorted_connections = self.sort_connections()
        
        i = 0
    
        while i < len(sorted_connections): 
            self.iterations += 1
            longest_connection = sorted_connections[i]
            swap_connection = self.find_swap(longest_connection)
        
            if not swap_connection:
                i += 1
                continue
        
            self.swap(longest_connection, swap_connection)
            i = 0
            self.sort_connections()

        # set district cables
        self.set_district_cables(self.district)
        return self.district
        
        
    def sort_connections(self):
        """Creates sorted list of the current battery house connections sorted by length.

        Returns
        ----------
        list
        """
        # create battery house list
        connection_list =[]
        for battery in self.district.batteries:
            houses = self.district.connections[battery.id]

            for house in houses:
                connection_list.append([battery, house])

        return connection_list.sort(key=lambda connection: self.calc_dist(connection[1].location, connection[0].location), reverse=True)

    def find_swap(self, connection):
        """Looks for a house with a beneficial swap possibility.

        Parameters
        ----------
        connection : tuple

        Returns
        ----------
        list
        """

        current_battery, current_house = connection
        current_dist = self.calc_dist(current_house.location, current_battery.location)

        # capacity left in the battery
        remaining_capacity = current_battery.capacity - (self.district.get_usage(current_battery) - current_house.output)

        best_length = float('inf')
        best_connection = None

        for new_house in self.district.houses:

            # check if the swap is allowed regarding output, else move to next house
            if new_house.output > remaining_capacity:
                continue

            new_battery = self.district.get_house_battery(new_house)

            if current_house.output > new_battery.capacity - (self.district.get_usage(new_battery) - new_house.output):
                continue
        
            # check if the swap would lead to less cables 
            current_total_dist = current_dist + self.calc_dist(new_house.location, new_battery.location)
            new_total_dist = self.calc_dist(current_house.location, new_battery.location) + self.calc_dist(new_house.location, current_battery.location)

            # check if it's the best swapping option
            if (new_total_dist < current_total_dist) and (new_total_dist < best_length):
                best_length = new_total_dist
                best_connection = [new_battery, new_house]
    
        # return best swapping option
        return best_connection


    def swap(self, current_connection, swap_connection):
        """Swaps batteries between two houses, and creates new cables.

        Parameters
        ----------
        current_connection : tuple

        swap_connection : tuple
        """
        current_battery, current_house = current_connection
        swap_battery, swap_house = swap_connection

        # remove current connections
        self.district.connections[current_battery.id].remove(current_house)
        self.district.connections[swap_battery.id].remove(swap_house)

        # make new connections
        self.district.connections[current_battery.id].append(swap_house)
        self.district.connections[swap_battery.id].append(current_house)