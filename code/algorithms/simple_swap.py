import numpy as np
import time
import copy
from .algorithm import Algorithm

class SimpleSwap(Algorithm):
    """
    Optimizing solution found by Manhattan distance based configuration, 
    based on the swapping of similar houses to a closer battery.
    """

    def __init__(self, district):
        self.district_copy = copy.deepcopy(self.district)

    
    def run(self):

        print()
        print("========== optimizing... (simple_swap algorithm) ===========")
        print()

        # sort connections based on length
        sorted_connections = sort_connections(self.district_copy)
        i = 0
    
    while i < len(sorted_cables): # and swapcount is not 0
        time.sleep(0.2)
        current_cable = sorted_cables[i]
        target_house = find_swap(current_cable, copied_district)
        
        if not target_house:
            i += 1
            print(f"list position: {i}")
            continue
        
        swap(current_cable.house, target_house, copied_district)
        i = 0
        sorted_cables = sort_cables(sorted_cables)
    
    return copied_district
        
        
def sort_cables(cables):
    """
    Returns sorted list of cables
    """
    # sort list based on length
    return sorted(cables, key=lambda cable: cable.calc_length(), reverse=True)

def find_swap(cable, district):
    """
    Looks for a house with a beneficial swap possibility
    """
    houses = district.houses
    left_own_battery = cable.battery.capacity - cable.battery.usage
    new_best_length = float('inf')
    might_swap_house = None

    for house in houses:
        # check if the swap is allowed regarding output, else move to next house
        if house.output > cable.house.output + left_own_battery:
            continue
        
        # check if the swap would lead to less cables
        current_total_cables = man_dist(house.location, house.get_battery().location) + man_dist(cable.house.location, cable.battery.location)
        new_total_cables = man_dist(house.location, cable.battery.location) + man_dist(house.get_battery().location, cable.house.location)

        # check if it's the best swapping option
        if (new_total_cables <= current_total_cables) and (new_total_cables < new_best_length):
            new_best_length = new_total_cables
            might_swap_house = house
    
    # return best swapping option
    return might_swap_house


def swap(house1, house2, district):
    """
    Swaps batteries between two houses, and creates new cables
    """
    battery1 = house1.cable.battery
    battery2 = house2.cable.battery

    # remove old cables
    district.remove_cable(house1.cable)
    district.remove_cable(house2.cable)

    # add new cables
    district.add_cable(battery2, house1)
    district.add_cable(battery1, house2)

    

def man_dist(point1, point2):
    """
    Calculates Manhattan distance between two grid points
    """
    x1, y1 = point1
    x2, y2 = point2

    return abs(x1 - x2) + abs(y1 - y2)