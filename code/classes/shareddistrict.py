import csv
import random

from .battery import Battery
from .house import House
from .sharedcable import Cable
from .connectpoint import Connectpoint

BATTERY_COST = 5000

class District():
    def __init__(self, uid, batteries_file, houses_file):
        self.id = uid
        self.batteries = self.load_batteries(batteries_file)
        self.houses = self.load_houses(houses_file)
        self.connectpoints = self.init_connectpoints()
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
                battery = Battery(i, location, capacity, BATTERY_COST)
                batteries.append(battery)

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

    def init_connectpoints(self):
        """
        Loads the first connectpoints of the district
        """
        connectpoints = []

        for battery in self.batteries:
            connectpoint = Connectpoint(battery.location, battery)
            connectpoints.append(connectpoint)

        return connectpoints


    def reset_connectpoints(self):
        """
        Resets the connectpoints to starting position
        """
        self.connectpoints = self.init_connectpoints()

    
    def add_cable(self, connectpoint, house):
        """
        Adds a cable object
        """
        battery = connectpoint.battery
        cable = Cable(connectpoint, battery, house)

        # update the connectpoints
        self.update_connectpoints(connectpoint, cable)

        battery.add_house(house)
        battery.add_cable(cable)

        house.add_cable(cable)

        self.cables.append(cable)

        # update the usage of the battery
        #connectpoint.update_usage(house)

    
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

    def get_connectpoints(self):
        """
        Returns a list of connectpoints
        """
        return self.connectpoints

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


    def update_connectpoints(self, connectpoint, cable):
        """
        Updates the connectpoints according to the cable path
        """

        #goal = connectpoint.get_location()
        battery = connectpoint.get_battery()

        path = cable.get_path()

        # remove the goal coordinates from the path
        path = path[:-1]

        # add every path coordinate to the connectpoints
        for location in path:

            new_point = Connectpoint(location, battery)
            self.connectpoints.append(new_point)
    

