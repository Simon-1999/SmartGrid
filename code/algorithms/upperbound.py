from .algorithm import Algorithm

class UpperBound(Algorithm):

    def run(self):

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
        """

        batteries = self.district.batteries
        
        return max(batteries, key=lambda battery: self.calc_dist(house.location, battery.location))