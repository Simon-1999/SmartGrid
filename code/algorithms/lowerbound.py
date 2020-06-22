"""Method to calculate the lowerbound of the problem based on closest batteries, assuming capacity
and house output do not matter. 
"""

from .algorithm import Algorithm

class LowerBound(Algorithm):
    """Calculates the lowerbound of the problem by just connecting houses to their closest batteries,
    overlooking any capacity problems. 

    Methods
    ----------
    run()
        Runs Lowerbound algorithm

    get_nearest_battery(house)
        Finds the nearest battery to a house
    """

    def run(self):
        """Runs the Lowerbound algorithm.

        Returns 
        ----------
        District object
            District with connections made for closest batteries
        """

        # loop through all the houses:
        for house in self.district.houses:

            # get nearest battery
            battery = self.get_nearest_battery(house)

            # connect house and battery
            self.district.add_connection(battery, house)

        # print results
        self.print_result(self.district)

        # return district
        return self.district


    def get_nearest_battery(self, house):
        """
        Calculates which battery in the list is the nearest to the given house.

        Parameters
        ----------
        house : House object

        Returns
        ----------
        Battery object
        """

        batteries = self.district.batteries
        
        batteries.sort(key=lambda battery: self.calc_dist(house.location, battery.location))
    
        return batteries[0]