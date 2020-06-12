import copy
import random

from .algorithm import Algorithm

class GroupSwap(Algorithm):
    """
    Swaps longest cables with different sizes
    """

    def __init__(self, district):

        self.district = copy.deepcopy(district) 
        self.groupsizes = [50, 20] 
        self.iterations = 0
        self.best_solution = copy.deepcopy(district)

    def run(self):

        print("group_swap running...")

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

                # asign new cables
                if self.asign_cables():

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
        """
        Removes cables from district
        """

        for cable in cables:

            self.district.remove_cable(cable)

    def asign_cables(self):
        """
        Assign house to cable an add cable
        """

        # random shuffle houses list
        random.shuffle(self.district.get_houses())

        # asign all free houses to nearest free battery
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
        """
        returns list of longest cables of size groupsize
        """

        # sort cables on length
        self.district.get_cables().sort(key=lambda cable: cable.calc_length() \
            , reverse=True)

        return self.district.get_cables()[:groupsize]

    def get_nearest_free_battery(self, house):
        """
        returns nearest free battery
        """

        # sort list of batteries on distance from house
        self.district.get_batteries().sort(key=lambda battery: \
            self.calc_dist(battery.get_location(), house.get_location()))

        # return first free battery found
        for battery in self.district.get_batteries():

            if not battery.calc_overload(house):
                return battery

        return None
