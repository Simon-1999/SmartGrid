""" Finds a solution by randomly connecting houses to batteries until a valid configuration emerges.

The algorithm the shuffles the list of houses in the district and connects each house 
to a remaining battery with the most capacity left. This process is repeated until a valid solution is found.
"""

import random 

from .algorithm import Algorithm

class Randomize(Algorithm):
    """ Randomly connects houses to batteries in a district and returns the district once a valid solution is found.

    The algorithm shuffles the list of houses in the district randomly, loops through the list of houses and creates 
    a connection between each house and a battery with the most capacity left from the batteries in the district.
    After checking if the configuration is valid, it either sets the district cables and returns the valid district 
    or it resets the district and runs again.

    Methods
    ----------
    run()
        Runs the algorithm

    assign_connections()
        Assigns the individual houses to a battery

    calc_least_used_batt()
        Returns the battery with the lowest usage in the district
    """

    def run(self):
        """Runs the Randomize algorithm.

        Returns
        ----------
        District object
            A valid random district configuration
        """

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
        """Assign houses to batteries and creates connections
        """

        # loop through all houses
        for house in self.district.houses:

            # get least used battery
            battery = self.calc_least_used_batt()

            # add cable 
            self.district.add_connection(battery, house)


    def calc_least_used_batt(self):
        """Calculate least used battery
        
        Returns
        ----------
        Battery object
        """

        return min(self.district.batteries, key=lambda \
            battery: self.district.get_usage(battery))
