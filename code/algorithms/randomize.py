import random 
import numpy as np 

def random_solution(district):
    """ 
    Finding random solution 
    """

    batteries = district.get_batteries()
    houses = district.get_houses()
    i = 0
    
    # making configurations until no battery is overloaded
    while True:

        # remove cable connections
        district.reset_cables()

        # randomize houses list
        randomize_houses(houses)

        # add cable connections
        add_cables(district, batteries, houses)

        if not district.is_overload():
            break
        
        i += 1

    print(f"RANDOM SOLUTION FOUND in {i} iterations")
    print_usage(district)

def randomize_houses(houses):
    """
    Randomize houses list
    """

    return random.shuffle(houses)    

def add_cables(district, batteries, houses):
    """
    Assign houses to batteries
    """

    for house in houses:
        usages = []
        for battery in batteries:
            usages.append(battery.usage)
        
        least_used_batt = batteries[np.argmin(usages)]

        # add cable between the house and the chosen battery
        district.add_cable(least_used_batt, house)

            
def print_usage(district):
    batteries = district.get_batteries()

    for battery in batteries:
        print(battery.usage)
