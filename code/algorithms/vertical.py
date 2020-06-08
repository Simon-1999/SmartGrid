import numpy as np 

def vertical_solution(district):
    """ 
    Finding solution with vertical sortign of houses and batteries
    """

    print("--- Running vertical solution ---")

    # make sure district is reset
    district.reset_cables()

    # query values
    batteries = district.get_batteries()
    houses = district.get_houses()
     
    # vertical order houses and batteries
    vertical_order_houses(houses)
    vertical_order_batteries(batteries)

    # add cable connections
    add_cables(district, batteries, houses)

    i = 1
    print(f"VERTICAL SOLUTION FOUND in {i} iterations")
    print_usage(district)

def add_cables(district, batteries, houses):
    """
    Assign houses to batteries
    """

    # loop through all houses
    for house in houses:

        # connect house to battery
        district.add_cable(nearest_free_battery(house, batteries), house)
          
def print_usage(district):
    """
    Print usage per battery in district
    """

    for battery in district.get_batteries():
        print(f"battery{battery.id}: {battery.usage}")

def nearest_free_battery(house, batteries):
    """
    Find nearest free battery
    """

    # loop through all batteries
    for battery in batteries:

        # returns first found free battery
        if battery.usage + house.output <= 1507:
            nearest_battery = battery
            break

    return nearest_battery

def vertical_order_houses(houses):
    """
    Order houses on vertical position
    """

    houses.sort(key=vertical_location, reverse=True)

def vertical_order_batteries(batteries):
    """
    Order batteries on vertical position
    """

    batteries.sort(key=vertical_location, reverse=True)

def vertical_location(obj):
    """
    Returns vertical position of object
    """

    return obj.get_location()[1]
        