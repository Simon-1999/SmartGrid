import random
from .algorithm import Algorithm

class RandomOptimize(Algorithm):
    """
    Finds a solution by connecting houses to the nearest battery with free capacity
    """
    def run(self):    

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
        """
        Assign houses to batteries
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
        """

        possible_batteries = self.district.get_possible_batteries(house)

        if not possible_batteries:
            return None
    
        return min(possible_batteries, key=lambda battery: self.calc_dist(house.location, battery.location))
        