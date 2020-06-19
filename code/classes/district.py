import csv

from .battery import Battery
from .house import House
from .final_cable import Cable

BATTERY_COST = 5000

class District():
    def __init__(self, uid, batteries_file, houses_file):
        self.id = uid
        self.connections = {}
        self.batteries = self.load_batteries(batteries_file)
        self.houses = self.load_houses(houses_file)
        self.cables = {}

    def load_batteries(self, file_path):
        """
        Loads all the batteries into the district and initialize connections dictionary
        """

        batteries = []
        with open(file_path, 'r') as in_file:
            reader = csv.DictReader(in_file)

            for i, row in enumerate(reader):
                # convert the location coordinates in a tuple of integers
                location = tuple(map(int, row["positie"].split(",")))

                capacity = float(row["capaciteit"])
                batteries.append(Battery(i, location, capacity, BATTERY_COST))
                self.connections[i] = []

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

    def add_connection(self, battery, house):
        """
        Connect house to battery
        """

        self.connections[battery.id].append(house)

    def remove_connection(self, battery, house):
        """
        Removes connected house from battery 
        """

        self.connections[battery.id].remove(house)

    def set_connections(self, connections):
        """
        Sets a the district to the given connections
        """

        self.connections = connections

    def reset_connections(self):
        """
        Resets the connections between the batteries and houses
        """

        for battery in self.batteries:
            self.connections[battery.id] = []

    def add_cable(self, battery, house):
        """
        Adds a cable object
        """

        cable = Cable(battery, house)
        self.cables.append(cable)

    def remove_cable(self, cable):
        """
        Removes the cable from the list of cables
        """

        self.cables.remove(cable)
        del cable

    def get_cables(self):
        """
        Returns the list of cables in the district
        """

        return self.cables

    def reset_cables(self):
        """
        Remove all cables
        """
    
        cables = self.cables

        for cable in cables:
            del cable

        self.cables = []
 
    def get_houses(self):
        """
        Returns a list of house objects in the district
        """

        return self.houses

    

    def get_empty_house(self):
        """
        Returns an empty house
        """

        connected_houses = []
        for values in self.connections.values():
            connected_houses += values

     
        for house in self.houses:
            if house not in connected_houses:
                return house
        
        return None

    def get_batteries(self):
        """
        Returns a list of battery objects in the district
        """

        return self.batteries

    def get_possible_batteries(self, house):
        """
        Returns a list of batteries a house can connect to
        """
        empty_batteries = []
        for battery in self.batteries:
            if not self.calc_overload(battery, house):
                empty_batteries.append(battery)
        
        return empty_batteries

    def get_usage(self, battery):

        usage = 0
        
        for house in self.connections[battery.id]:
            usage += house.output

        return usage

    def is_overload(self):
        """
        Returns if the usage exceeds capacity
        """
        
        for battery in self.batteries:

            if self.get_usage(battery) > battery.capacity:
                return True
        
        return False

    def calc_overload(self, battery, house):
        """
        Returns if house output exceeds battery capacity
        """

        return self.get_usage(battery) + house.output > battery.capacity

    def calc_battery_connections_costs(self, battery):
        """
        Calculates costs of connection to battery
        """

        houses = self.connections[battery.id]
        costs = 0

        for house in houses:
            costs += self.calc_dist(house, battery) * 9

        return costs

    def calc_connection_costs(self):
        """
        Calculates the total cost of the district
        """

        connections_cost = 0
        batt_cost = 0

        for battery in self.batteries:
            batt_cost += battery.cost
            connections_cost += self.calc_battery_connections_costs(battery)

        costs = {
            "connections": connections_cost,
            "batteries": batt_cost,
            "total": connections_cost + batt_cost
        }

        return costs

    def calc_dist(self, object1, object2):
        """
        Calculates manhatten distance between two objects
        """

        x1, y1 = object1.location
        x2, y2 = object2.location

        return abs(x1 - x2) + abs(y1 - y2) 

    def all_houses_connected(self):
        """
        Checks if there are 150 cables
        """

        houses_connected = 0
        
        for houses in self.connections.values():
            houses_connected += len(houses)

        return houses_connected == 150
