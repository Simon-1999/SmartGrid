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

        self.district = copy.deepcopy(district) 
        self.groupsizes = [50, 20] 
        self.iterations = 0
        self.best_solution = copy.deepcopy(district)

    def run(self):
        """Runs the GroupSwap algorithm

        Returns
        ----------
        District object
            Lowest cost district the algorithm has found
        """

        min_costs = self.district.calc_costs()['total']
        solution_found = False
        random_iterations = 1000

        for groupsize in self.groupsizes:

            for i in range(random_iterations):

                # increments iterations
                self.iterations += 1
                
                # remove longest cables
                longest_cables = self.get_longest_cables(groupsize)
                self.remove_cables(longest_cables)

                # assign new cables
                if self.assign_cables():

                    # calculate costs
                    costs = self.district.calc_costs()['total']

                    # check if solution is better
                    if costs < min_costs:
                        # print(f"new: {costs}, improved: {min_costs - costs}, groupsize: {groupsize},iteration: {i}")   
                        min_costs = costs
                        self.best_solution = copy.deepcopy(self.district)
                        solution_found = True

            # for next group work with best found solution
            if solution_found:
                self.district = copy.deepcopy(self.best_solution)
                solution_found = False      
                                 
        self.print_result(self.best_solution)

        print("group_swap done")

        return self.best_solution

    def remove_cables(self, cables):
        """Removes cables from a district.

        Parameters
        ----------
        cables : list
            Cables to remove from the district
        """

        for cable in cables:

            self.district.remove_cable(cable)

    def assign_cables(self):
        """Assign house to cable an add this information to the district.

        Returns
        ----------
        bool
        """

        # random shuffle houses list
        random.shuffle(self.district.get_houses())

        # assign all free houses to nearest free battery
        for house in self.district.get_houses():

            # assign free house to battery
            if not house.has_cable():
                battery = self.get_nearest_free_battery(house)

                # check if there is a free battery
                if battery == None:
                    return False

                # add cable
                self.district.add_cable(battery, house)

        return True

    def get_longest_cables(self, groupsize):
        """Returns list of longest cables in the district of size groupsize

        Parameters
        ----------
        groupsize : int

        Returns
        ----------
        list
        """

        # sort cables on length
        self.district.get_cables().sort(key=lambda cable: cable.calc_length() \
            , reverse=True)

        return self.district.get_cables()[:groupsize]

    def get_nearest_free_battery(self, house):
        """Returns the nearest available battery to a house. 

        Parameters
        ----------
        house : House object

        Returns
        ---------
        Battery object
        """

        # sort list of batteries on distance from house
        self.district.get_batteries().sort(key=lambda battery: \
            self.calc_dist(battery.get_location(), house.get_location()))

        # return first free battery found
        for battery in self.district.get_batteries():

            if not battery.calc_overload(house):
                return battery

        return None
