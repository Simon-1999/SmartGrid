"""Method to calculate the upperbound of the problem based on furthest batteries, assuming capacity
and house output do not matter. 
"""

from .algorithm import Algorithm

class UpperBound(Algorithm):
    """Calculates the upperbound of the problem by just connecting houses to their furthes batteries,
    overlooking any capacity problems. 

    Methods
    ----------
    run()
        Runs Lowerbound algorithm

    get_furthes_battery(house)
        Finds the furthest battery to a house
    """

    def run(self):
        """Runs the Lowerbound algorithm.

        Returns 
        ----------
        District object
            District with connections made for furthest batteries
        """

        # loop through all the houses:
        for house in self.district.houses:

            # get nearest battery
            battery = self.get_furthest_battery(house)

            # connect house and battery
            self.district.add_connection(battery, house)

        # set district cables
        self.set_district_cables(self.district)

        # return district
        return self.district

    def get_furthest_battery(self, house):
        """
        Calculates which battery in the list is the furthest to the given house

        Parameters
        ----------
        house : House object

        Returns
        ----------
        Battery object
        """

        batteries = self.district.batteries
        
        return max(batteries, key=lambda battery: self.calc_dist(house.location, battery.location))