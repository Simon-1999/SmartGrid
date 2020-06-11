"""
Explanation of file:
Random shuffling houses untill solution is found
Status: 
"""

# imports
import random 
import copy

def run(district):
    """ 
    Shuffling houses and finding random solution
    """

    print(f"====== randomize running ======")

    # copy district
    district = copy.deepcopy(district)

    # query values
    batteries = district.get_batteries()
    houses = district.get_houses()

    # initialize algorithm iterations
    i = 0
    
    # making configurations until no battery is overloaded
    while True:

        # remove cable connections
        district.reset_cables()

        # randomize houses list
        order_randomize(houses)

        # add cable connections
        add_cables(district, batteries, houses)

        # check if configuration is valid
        if not district.is_overload():
            break
        
        # increment iterations
        i += 1

    print_result(district, i)
    print(f"======== randomize done ========")

    return district

def order_randomize(list_objects):
    """
    Random shuffles input list
    """

    return random.shuffle(list_objects)    

def add_cables(district, batteries, houses):
    """
    Assign houses to batteries
    """

    # loop through all houses
    for house in houses:

        # get least used battery
        least_used_batt = calc_least_used_batt(batteries)

        # add cable between house and battery
        district.add_cable(least_used_batt, house)

def calc_least_used_batt(batteries):
    """
    Calculate least used battery
    """

    return min(batteries, key=lambda battery: battery.usage)

def print_result(district, iterations):

    print("+------------------------------+")
    if district.is_overload():
        print(f"| {'configuration:':<15} {'invalid':>12} |")
    else:
        print(f"| {'configuration:':<15} {'valid':>12} |")
    print(f"| {'iterations:':<15} {iterations:>12} |")
    costs = district.calc_costs()
    print(f"| {'cables:':<15} {costs['cables']:>12} |")
    print(f"| {'batteries:':<15} {costs['batteries']:>12} |")
    print(f"| {'total:':<15} {costs['total']:>12} |")
    print("+------------------------------+")   
