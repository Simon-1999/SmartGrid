"""Representation of a a SmartGrid district. A district is defined by its batteries and
houses, and an ID. Next, while running any algorithm, connections and cables are added to create a 
final configuration. 
"""

import csv

from .battery import Battery
from .house import House

BATTERY_COST = 5000

class District():
    """This class upholds a data structure for a SmartGrid with houses and batteries, and creates the
    possibility to add connections and unique or shared cables between houses and batteries. All information
    regarding energy capacities and outputs are also stored appropriately. 

    Methods
    ----------
    load_batteries(file_path)
        Loads batteries into district

    load_houses(file_path)
        Loads houses into district

    add_connection(battery, house)
        Connects house to a battery

    remove_connection(battery, house)
        Removes specific connection from the configuration

    set_connections(connections)
        Sets connections in a district to a given configuration

    reset_connections()
        Resets the whole district

    add_cable(house, path)
        Adds a cable path to the specified house

    reset_cables()
        Remove all cable data from the district
        
    def get_empty_house()
        Find a house that is not yet connected

    get_possible_batteries(house)
        Get all available batteries for a house

    get_usage(battery)
        Get current usage by connections of a battery

    is_overload()
        Check if district has a valid configuration

    calc_overload(battery, house)
        Check if a house would overload a battery when connected

    calc_battery_connections_costs(battery)
        Calculate costs of all connections to a battery

    calc_connection_costs()
        Calculate costs of a unique district

    calc_cables_costs()
        Calculate costs of a shared district

    calc_dist(object1, object2)
        Calculate Manhattan distance between two objects in the district
    
    all_houses_connected()
        Check if all houses have a unique cable

    print_district_status()
        Prints a general overview of the status of the district parameters
        

    """

    def __init__(self, uid, batteries_file, houses_file):
        """Parameters
        ----------
        uid : int

        batteries_file : .csv-file

        houses_file : .csv_file
        """
        self.id = uid
        self.connections = {}
        self.batteries = self.load_batteries(batteries_file)
        self.houses = self.load_houses(houses_file)
        self.cables = {}


    def load_batteries(self, file_path):
        """
        Loads all the batteries into the district and initializes connections dictionary.

        Parameters
        ----------
        file_path : str

        Returns
        ----------
        list
            List of dictionaries with battery data
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
        Loads all the houses into the district and initializes connections dictionary.

        Parameters
        ----------
        file_path : str

        Returns
        ----------
        list
            List with house data
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
        """Connects house to battery by modifying battery data.

        Parameters
        ----------
        battery : Battery object

        house : House object
        """

        self.connections[battery.id].append(house)


    def remove_connection(self, battery, house):
        """Removes house from battery by modifying battery data.

        Parameters
        ----------
        battery : Battery object

        house : House object
        """

        self.connections[battery.id].remove(house)


    def set_connections(self, connections):
        """Modifies a district to contain the given connections. 

        Parameters
        ----------
        connections : dict
        """

        self.connections = connections


    def reset_connections(self):
        """Resets the connections between the batteries and houses by removing all stored information.
        """

        for battery in self.batteries:
            self.connections[battery.id] = []

    def add_cable(self, house, path):
        """Adds a cable path to the specified house

        Parameters
        ----------
        house: House object
        path: list
        """

        self.cables[house.id] = path
            

    def reset_cables(self):
        """Remove all cables in a district.
        """
    
        self.cables = {}
    

    def get_empty_house(self):
        """Returns a house that is not yet connected, if there is one.

        Returns
        ----------
        House object
        """

        connected_houses = []
        for values in self.connections.values():
            connected_houses += values

     
        for house in self.houses:
            if house not in connected_houses:
                return house
        
        return None

    def get_empty_houses(self):
        """Returns houses hat are not yet connected, if there is one.

        Returns
        ----------
        list
        """

        connected_houses = []
        empty_houses = []

        for values in self.connections.values():
            connected_houses += values

     
        for house in self.houses:
            if house not in connected_houses:
                empty_houses.append(house)
        
        return empty_houses


    def get_possible_batteries(self, house):
        """Returns a list of batteries a house can connect to regarding battery capacity and house output.

        Parameters
        ----------
        house : House object

        Returns
        ----------
        list
        """

        empty_batteries = []
        for battery in self.batteries:
            if not self.calc_overload(battery, house):
                empty_batteries.append(battery)
        
        return empty_batteries


    def get_usage(self, battery):
        """Calculates how much of the battery capacity is currently being used by connected houses.

        Parameters
        ----------
        battery : Battery object

        Returns
        ----------
        float
        """
        usage = 0
        
        for house in self.connections[battery.id]:
            usage += house.output

        return usage

    def is_overload(self):
        """Returns if the usage of any battery exceeds capacity.

        Returns
        ----------
        bool
        """
        
        for battery in self.batteries:

            if self.get_usage(battery) > battery.capacity:
                return True
        
        return False


    def calc_overload(self, battery, house):
        """Returns if house output would exceed battery capacity if connected.

        Parameters
        ----------
        battery : Battery object

        house : House object

        Returns
        ----------
        bool
        """

        return self.get_usage(battery) + house.output > battery.capacity

    def calc_battery_connections_costs(self, battery):
        """Calculates costs of current connections to given battery.

        Parameters
        ----------
        battery : Battery object

        Returns
        ----------
        int
        """

        houses = self.connections[battery.id]
        costs = 0

        for house in houses:
            costs += self.calc_dist(house, battery) * 9

        return costs


    def calc_connection_costs(self):
        """Calculates the total cost of the district, adding battery costs and connections costs.

        Returns
        ----------
        dict
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


    def calc_cables_costs(self):
        """Calculates the total cost of the district with shared cables instead of unique connections.

        Returns
        ----------
        dict
        """

        cables_cost = 0
        batt_cost = 0
        for battery in self.batteries:
            batt_cost += battery.cost
        
        for path in self.cables.values():
            cables_cost += (len(path) - 1) * 9
        
        costs = {
            "cables": cables_cost,
            "batteries": batt_cost,
            "total": cables_cost + batt_cost
        }

        return costs


    def calc_dist(self, object1, object2):
        """Calculates manhatten distance between two objects.

        Returns
        ----------
        int
        """

        x1, y1 = object1.location
        x2, y2 = object2.location

        return abs(x1 - x2) + abs(y1 - y2) 


    def all_houses_connected(self):
        """Checks if there are 150 cables in a unique cable district.

        Returns
        ----------
        bool
        """

        houses_connected = 0
        
        for houses in self.connections.values():
            houses_connected += len(houses)

        return houses_connected == 150

    def get_house_battery(self, house):

        for battery in self.district.batteries:
            houses = self.district.connections[battery.id]

            if house in houses:
                return battery

    def print_district_status(self):
        """Prints a general overview of the status of the district parameters
        """

        print("+---------------------------------+")
        if not self.is_overload() and self.all_houses_connected():
            print(f"| {'configuration:':<18} {'valid':>12} |")
        else:
            print(f"| {'configuration:':<18} {'invalid':>12} |")
        costs = district.calc_cables_costs()
        print(f"| {'connections:':<18} {costs['connections']:>12} |")
        print(f"| {'batteries:':<18} {costs['batteries']:>12} |")
        print(f"| {'total:':<18} {costs['total']:>12} |")
        print("+---------------------------------+")  
