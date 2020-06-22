from .algorithm import Algorithm

class UpperBound(Algorithm):

    def run(self):

        # loop through all the houses:
        for house in self.district.houses:

            # get nearest battery
            battery = self.get_furthest_battery(house)

            # connect house and battery
            self.district.add_connection(battery, house)

        # print results
        self.print_result(self.district)

        # return district
        return self.district

    def get_furthest_battery(self, house):
        """
        Calculates which battery in the list is the nearest to the given house
        """

        batteries = self.district.batteries
        
        batteries.sort(key=lambda battery: self.calc_dist(house.location, battery.location), reverse=True)
    
        return batteries[0]