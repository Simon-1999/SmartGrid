"""
Explanation of file:
Random shuffling houses untill solution is found
Status: 
"""

import random 
from .algorithm import Algorithm

class Randomize(Algorithm):
    """
    Random shuffling houses untill solution is found
    """

    def run(self):

        while True:

            self.iterations += 1

            # randomize houses list
            random.shuffle(self.district.houses)

            # add cable connections
            self.assign_connections()

            # check if configuration is valid
            if not self.district.is_overload():
                break

            self.district.reset_connections()

        # set district cables
        self.set_district_cables(self.district)

        return self.district

    def assign_connections(self):
        """
        Assign houses to batteries
        """

        # loop through all houses
        for house in self.district.houses:

            # get least used battery
            battery = self.calc_least_used_batt()

            # add cable 
            self.district.add_connection(battery, house)

    def calc_least_used_batt(self):
        """
        Calculate least used battery
        """

        return min(self.district.batteries, key=lambda \
            battery: self.district.get_usage(battery))
