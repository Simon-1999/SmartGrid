import csv

from .battery import Battery
from .house import House
from .cable import Cable


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

                # conver the location coordinates in a tuple
                location = tuple(row["positie"].split(","))
                capacity = row["capaciteit"]
                batteries.append(Battery(i, location, capacity))

        return batteries

    def load_houses(self, file_path):
        """
        Loads all the houses into the district
        """
        
        houses = []
        with open(file_path, 'r') as in_file:
            reader = csv.DictReader(in_file)
            
            for i, row in enumerate(reader):
                location = tuple((row["x"], row["y"]))
                output = row["maxoutput"]
                houses.append(House(i, location, output))

        return houses

    
    def add_cable(self, battery, house):
        """
        Adds a cable object
        """
        cable = Cable(battery,house)

        self.cables.append(cable)

        # update the usage of the battery
        battery.update_usage(house)

    
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


    def check_capacities(self):
        """
        Returns if the usage of all batteries are within capacity
        """

        for battery in self.batteries:

            if not battery.check_capacity():
                return False
        
        return True

    def reset_cables(self):
        """
        Resets the connections between the batteries and houses
        """

        self.cables = []

        for battery in self.batteries:
            battery.reset_usage()


    def calculate_cost(self):
        pass

    def draw_district(self):
        pass




