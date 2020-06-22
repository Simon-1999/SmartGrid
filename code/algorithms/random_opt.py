import random
from .algorithm import Algorithm

class RandomOptimize(Algorithm):
    """
    Finds a solution by connecting houses to the neirest battery with free capacity
    """
    def run(self):    

        while True:

            self.iterations += 1
            print(self.iterations)
        
            # randomize houses list
            self.order_random(self.district.get_houses())

            self.assign_connections()

            if not self.district.is_overload() and self.district.all_houses_connected():
                break

            self.district.reset_connections()

        self.print_result(self.district)

        self.set_district_cables(self.district)

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

            battery = self.get_nearest_battery(house)

            if not battery:
                return

            # add connection
            self.district.add_connection(battery, house)


    def get_nearest_battery(self, house):
        """
        Calculates which battery in the list is the nearest to the given house
        """

        possible_batteries = self.district.get_possible_batteries(house)
        
        possible_batteries.sort(key=lambda battery: self.calc_dist(house.location, battery.location))

        if not possible_batteries:
            return None
    
        return possible_batteries[0]