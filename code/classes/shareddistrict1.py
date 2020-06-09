import csv

from .sharedbattery1 import Battery
from .sharedhouse1 import House
from .sharedcable1 import Cable
from .connectpoint import Connectpoint


class District():
    def __init__(self, uid, batteries_file, houses_file):
        self.id = uid
        self.connectpoints = []
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
                battery = Battery(i, location, capacity)
                batteries.append(battery)

                # add the battery connect points
                connectpoint = Connectpoint(location, battery)
                self.connectpoints.append(connectpoint)

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

    
    def add_cable(self, connectpoint, house):
        """
        Adds a cable object
        """
        cable = Cable(connectpoint, house)

        # update the connectpoints
        self.update_connectpoints(connectpoint, cable)
        
        house.add_cable(cable)

        self.cables.append(cable)

        # update the usage of the battery
        connectpoint.update_usage(house)

    
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

    def check_houses(self):
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
        #path.remove(goal)

        # add every path coordinate to the connectpoints
        for location in path:

            new_point = Connectpoint(location, battery)
            self.connectpoints.append(new_point)
    

