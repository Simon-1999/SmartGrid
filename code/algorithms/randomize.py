import random 

def random_solution(district):
    """ 
    Finding random solution 
    """

    batteries = district.get_batteries()
    houses = district.get_houses()
    
    # making configurations until no battery is overloaded
    while(overload == True):

        # remove cable connections
        district.reset_cables()

        # randomize houses list
        randomize_houses(houses)

        # add cable connections
        add_cables(batteries, houses)

        # check capacity of batteries
        overload = district.check_capacities()

    print("RANDOM SOLUTION FOUND")

def randomize_houses(houses):
    """
    Randomize houses list
    """

    return random.shuffle(houses)    

def add_cables(batteries, houses):
    """
    Assign houses to batteries
    """

    # loop through battery
    for battery in batteries:

        # loop through 30 houses
        for house in houses[(battery.id*30):(battery.id*30 + 30)]

            # add cable to 30 houses
            district.add_cable(battery, house)
            