"""Finds a solution by randomly connecting houses to the nearest battery with free capacity

The algortihm randomly connects each house to the nearest battery with remaining capacity. 
It repeats this until a valid configuration is found and returns the district with this configuration.
"""

import random

from .algorithm import Algorithm

class RandomOptimize(Algorithm):
    """ Randomly connects houses to the nearest batteries in a district and returns the district once a valid solution is found.

    The algorithm shuffles the list of houses in the district randomly, loops through the list of houses and creates 
    a connection between each house and the nearest battery with capacity left from the batteries in the district.
    After checking if the configuration is valid, it either sets the district cables and returns the valid district 
    or it resets the district and runs again.

    Methods
    ----------
    run()
        Runs the algorithm

    assign_connections()
        Assigns the individual houses to a battery

    get_nearest_free_battery()
        Returns the nearest free battery to the house
    
    """
    def run(self): 
        """Runs the Randomize algorithm.

        Returns
        ----------
        District object
            A valid optimized district configuration
        """   

        while True:

            self.iterations += 1
        
            # randomize houses list
            random.shuffle(self.district.houses)

            self.assign_connections()

            if not self.district.is_overload() and self.district.all_houses_connected():
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

            battery = self.get_nearest_free_battery(house)

            if not battery:
                return

            # add connection
            self.district.add_connection(battery, house)


    def get_nearest_free_battery(self, house):
        """
        Calculates which battery in the list is the nearest to the given house

        Paramaters
        ----------
        house : House object

        Returns
        ----------
        Battery object
        """

        possible_batteries = self.district.get_possible_batteries(house)

        if not possible_batteries:
            return None
    
        return min(possible_batteries, key=lambda battery: self.calc_dist(house.location, battery.location))
        