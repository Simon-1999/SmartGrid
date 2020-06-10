import csv

from .battery import Battery
from .house import House
from .cable import Cable

BATTERY_COST = 5000

class District():
    def __init__(self, uid, batteries_file, houses_file):
        self.id = uid
        self.batteries = self.load_batteries(batteries_file)
        self.houses = self.load_houses(houses_file)
        self.cables = []

    def load_batteries(self, file_path):
        """
        Loads all the batteries into the district
        """

        batteries = []
        with open(file_path, 'r') as in_file:
            reader = csv.DictReader(in_file)

            for i, row in enumerate(reader):

                # convert the location coordinates in a tuple of integers
                location = tuple(map(int, row["positie"].split(",")))

                capacity = float(row["capaciteit"])
                batteries.append(Battery(i, location, capacity, BATTERY_COST))

        return batteries

    def load_houses(self, file_path):
        """
        Loads all the houses into the district
        """
        
        houses = []
        with open(file_path, 'r') as in_file:
            reader = csv.DictReader(in_file)
            
            for i, row in enumerate(reader):
                location = tuple((int(row["x"]), int(row["y"])))
                output = float(row["maxoutput"])
                houses.append(House(i, location, output))

        return houses

    
    def add_cable(self, battery, house):
        """
        Adds a cable object
        """
        cable = Cable(battery, house)
        
        battery.add_house(house)
        battery.add_cable(cable)

        house.add_cable(cable)

        self.cables.append(cable)


    def remove_cable(self, cable):
        """
        Removes the cable from the list of cables and the corresponding battey and hous objects
        """
        # adjust if class attributes become private
        battery = cable.battery
        house = cable.house

        # adjust if class attributes become private
        battery.cable = None
        house.cable = None

        self.cables.remove(cable)

        del cable

    
    def get_batteries(self):
        """
        Returns a list of battery objects in the district
        """

        return self.batteries

    
    def get_houses(self):
        """
        Returns a list of house objects in the district
        """

        return self.houses


    def is_overload(self):
        """
        Returns if the usage of all batteries are within capacity
        """

        for battery in self.batteries:

            if battery.is_overload():
                return True
        
        return False

    def reset_cables(self):
        """
        Resets the connections between the batteries and houses
        """

        #for cable in self.cables:
            #del cable
        
        self.cables = []

        for battery in self.batteries:
            battery.reset_usage()

    def get_cables(self):
        """
        Returns the list of cables in the district
        """

        return self.cables


    def calc_costs(self):
        """
        Calculates the total cost of the district
        """

        cables_cost = 0
        batt_cost = 0

        # add the costs of the cables
        for cable in self.cables:
            cables_cost += cable.get_cost()

        # add the costs of the batteries
        for battery in self.batteries:
            batt_cost += battery.get_cost()

        costs = {
            "cables": cables_cost,
            "batteries": batt_cost,
            "total": cables_cost + batt_cost
        }

        return costs

    def all_houses_connected(self):
        """
        Checks if all the houses have a cable
        """

        for house in self.houses:

            if not house.has_cable():
                return False

        return True


