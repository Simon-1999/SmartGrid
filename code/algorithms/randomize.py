import random 

def random_solution(district):
    """ 
    Finding random solution 
    """

    batteries = district.get_batteries()
    houses = district.get_houses()
    
    # making configurations until no battery is overloaded
    for i in range(10):

        # remove cable connections
        district.reset_cables()

        # randomize houses list
        randomize_houses(houses)

        # add cable connections
        add_cables(district, batteries, houses)

        print_usage(district)
        if not district.is_overload():
            break
        
        print("solution not found, reset")

    print("RANDOM SOLUTION FOUND")

def randomize_houses(houses):
    """
    Randomize houses list
    """

    return random.shuffle(houses)    

def add_cables(district, batteries, houses):
    """
    Assign houses to batteries
    """

    # loop through battery
    for battery in batteries:

        # loop through 30 houses
        for house in houses[(battery.id*30):(battery.id*30 + 30)]:

            # add cable to 30 houses
            district.add_cable(battery, house)
            
def print_usage(district):
    batteries = district.get_batteries()

    for battery in batteries:
        print(battery.usage)
