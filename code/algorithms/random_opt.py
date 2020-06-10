
"""
Explanation of file:
Status: 
"""

def random_opt(district):
    """
    Finds a solution by connecting houses to the neirest battery with free capacity
    """

    # make sure district is reset
    district.reset_cables()

    # query values
    batteries = district.get_batteries()
    houses = district.get_houses()

    # make the connections
    add_cables(district, batteries, houses)

    # check if any of the batteries is overloaded
    success = district.is_overload() == False 

    return {"success": success}




def add_cables(district, batteries, houses):
    """
    Adds cable connections between the batteries and the houses
    """

    # loop through the houses
    for house in houses:

        # update the free batteries list
        free_batteries = available_batteries(batteries, house)

        # choose the nearest free battery to the house
        battery = nearest_battery(free_batteries, house)

        # connect the house and that battery
        district.add_cable(battery, house)

    

def available_batteries(batteries, house):
    """
    Returns a list of batteries that still have capacity left to add a cable
    """

    free_batteries = []

    for battery in batteries:

        # check if battery capacity is exceeded after adding the house
        if not battery.calc_overload(house):
            free_batteries.append(battery)

    return free_batteries


def nearest_battery(batteries, house):
    """
    Calculates which battery in the list is the nearest to the given house
    """

    # get the locations
    house_location = house.get_location()
    batt_location = batteries[0].get_location()

    # define the first battery in the list as the minimum distance
    min_dist = calc_manhattan_dist(house_location, batt_location)
    nearest_battery = batteries[0]

    # check if the other batteries are nearer to the house
    for battery in batteries:

        batt_location = battery.get_location()

        dist = calc_manhattan_dist(house_location, batt_location)

        if dist < min_dist:
            nearest_battery = battery
            min_dist = dist
    
    return nearest_battery


def calc_manhattan_dist(start, goal):
    """
    Calculates the manhattan distance from two tuple coordinates
    """

    # set the seperate start and goal coordinates
    x, y = start
    x_goal, y_goal = goal

    # calculate the absolute distances
    dist = abs(x - x_goal) + abs(y - y_goal)

    return dist
