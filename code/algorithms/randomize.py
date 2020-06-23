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

        print("randomize running... ")

        while True:

            self.iterations += 1

            # randomize houses list
            self.order_random(self.district.get_houses())

            # add cable connections
            self.assign_connections()

            # check if configuration is valid
            if not self.district.is_overload():
                break

            self.district.reset_connections()

        self.print_result(self.district)

        # set district cables
        self.set_district_cables(self.district)

        print("randomize done")

        return self.district

    def order_random(self, list_objects):
        """
        Random order house
        """

        return random.shuffle(list_objects)

    def assign_connections(self):
        """
        Assign houses to batteries
        """

        # loop through all houses
        for house in self.district.get_houses():

            # get least used battery
            battery = self.calc_least_used_batt()

            # add cable 
            self.district.add_connection(battery, house)

    def calc_least_used_batt(self):
        """
        Calculate least used battery
        """

        return min(self.district.get_batteries(), key=lambda \
            battery: self.district.get_usage(battery))
