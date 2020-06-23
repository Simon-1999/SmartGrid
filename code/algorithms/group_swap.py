"""Tries repeatedly to swap houses with a long cable with another house regarding their batteries, resulting in lower costs

The GroupSwap algorithm takes a configurated district as positional argument. The algorithm then takes out the longest cables and 
repeatedly takes a sample of these. If a new, random configuration of this sample results in lower costs, it is taken as the current
best solution. This goes on until after the specified amount of iterations.
"""

import copy
import random

from .algorithm import Algorithm

class GroupSwap(Algorithm):
    """Repeatedly reassigns longest district cables randomly for #iterations, returns the cheapest found district 

    GroupSwap respectively takes the 50 and then 20 longest cables of a district to pull a random sample from and to randomly reassign.
    This is repeated for every group size for the coded amount of random_iterations. The best found configuration is returned. 

    Attributes
    ----------
    district : District object
        An input district to perform the algorithm on

    groupsizes : list
        Group sizes to use, we use 50 and 20

    iterations : int
        Number of iterations done by the algorithm, starts at 0

    best_solution: District object
        To store the best solution in, this updates as the algorithm goes on

    Methods
    ----------
    run()
        Runs the algorithm

    remove_cables()
        Removes cables from the district

    assign_cables()
        Assigns free houses to available batteries

    get_longest_cables(groupsize)
        Returns the longest cables in the district

    get_nearest_free_battery(house)
        Returns nearest battery with enough free capacity
    """

    def __init__(self, district):
        """Parameters:
        ----------
        district : District object
        """

        self.district = district
        self.groupsizes = [50, 20] 
        self.iterations = 0
        self.best_solution = copy.deepcopy(district)
        self.min_costs = self.district.calc_connection_costs()['total']
        self.solution_found = False
        self.random_iterations = 1000

    def run(self):
        """Runs the GroupSwap algorithm

        Returns
        ----------
        District object
            Lowest cost district the algorithm has found
        """

        for groupsize in self.groupsizes:

            for i in range(self.random_iterations):

                # increments iterations
                self.iterations += 1

                # sort connections based on length
                sorted_connections = self.sort_connections()
                
                # remove longest connections
                self.remove_longest_connections(sorted_connections, groupsize)

                # assign new connections
                if self.assign_connections():

                    # calculate costs
                    costs = self.district.calc_connection_costs()['total']

                    # check if solution is better
                    if costs < self.min_costs:
                        # print(f"new: {costs}, improved: {min_costs - costs}, groupsize: {groupsize},iteration: {i}")   
                        self.min_costs = costs
                        self.best_solution = copy.deepcopy(self.district)
                        self.solution_found = True

            # for next group work with best found solution
            if self.solution_found:
                self.district = self.best_solution
                solution_found = False      
                                 
        self.print_result(self.best_solution)

        print("group_swap done")

        return self.district

    def assign_connections(self):
        """Assign house to cable an add this information to the district.

        Returns
        ----------
        bool
        """

        # random shuffle houses list
        random.shuffle(self.district.get_houses())

        # get empty houses
        empty_houses = self.district.get_empty_houses()

        # assign all free houses to nearest free battery
        for house in empty_houses:

                battery = self.get_nearest_free_battery(house)

                # check if there is a free battery
                if battery == None:
                    return False

                # add connection
                self.district.connections[battery.id].append(house)

        return True

    def remove_longest_connections(self, sorted_connections, groupsize):
        """Returns list of longest cables in the district of size groupsize

        Parameters
        ----------
        groupsize : int

        Returns
        ----------
        list
        """

        # get group of longest connections
        longest_connections = sorted_connections[:groupsize]
        
        # loop through the connections and remove the house from the battery in the connections dict
        for battery, house in longest_connections:
            self.district.connections[battery.id].remove(house)


    def sort_connections(self):
        """
        Creates sorted list of the current battery house connections sorted by length
        """
        # create battery house list
        # [[BATTERY, HOUSE], [BATTERY, HOUSE], etc.]
        connection_list =[]
        for battery in self.district.batteries:
            houses = self.district.connections[battery.id]

            for house in houses:
                connection_list.append([battery, house])

        return sorted(connection_list, key=lambda connection: self.calc_dist(connection[1].location, connection[0].location), reverse=True)


    def get_nearest_free_battery(self, house):
        """
        Calculates which battery in the list is the nearest to the given house
        """

        possible_batteries = self.district.get_possible_batteries(house)
        
        possible_batteries.sort(key=lambda battery: self.calc_dist(house.location, battery.location))

        if not possible_batteries:
            return None
    
        return possible_batteries[0]
