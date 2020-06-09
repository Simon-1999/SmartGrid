
from operator import attrgetter

def manhattan_solution(district):
    """
    Finds a solution by connecting houses to the neirest battery with free capacity
    """

    # make sure district is reset
    district.reset_cables()

    # vertical order batteries and houses and connectpoints
    batteries = district.get_batteries()
    order_vertical(batteries)
    houses = district.get_houses()
    order_vertical(houses)
    connectpoints = district.get_connectpoints()
    order_vertical(connectpoints)

    # make the connections
    if not add_cables(district, connectpoints, houses):
        return {"success": False}

    # check if any of the batteries is overloaded
    success = district.is_overload() == False 

    return {"success": success}

def add_cables(district, connectpoints, houses):
    """
    Adds cable connections between the batteries and the houses
    """
    i = 0
    # loop through the houses
    for house in houses:

        i += 1
        print(f"{i}")

        # update the free connectpoints list
        free_connectpoints = available_connectpoints(connectpoints, house)

        if not free_connectpoints:
            return False

        # choose the nearest free battery to the house
        connectpoint = nearest_connectpoint(free_connectpoints, house)

        # connect the house and that battery
        district.add_cable(connectpoint, house)
    
    return True 

def available_connectpoints(connectpoints, house):
    """
    Returns a list of connectpoints that still have capacity left to add a cable
    """

    free_connectpoints = []

    for connectpoint in connectpoints:

        battery = connectpoint.get_battery()

        # check if battery capacity is exceeded after adding the house
        if not battery.calc_overload(house):
            free_connectpoints.append(connectpoint)

    return free_connectpoints


def nearest_connectpoint(connectpoints, house):
    """
    Calculates which battery in the list is the nearest to the given house
    """

    # get the locations
    house_location = house.get_location()
    connect_location = connectpoints[0].get_location()

    # define the first battery in the list as the minimum distance
    min_dist = calc_manhattan_dist(house_location, connect_location)
    nearest_connectpoint = connectpoints[0]

    # check if the other batteries are nearer to the house
    for connectpoint in connectpoints:

        connect_location = connectpoint.get_location()

        dist = calc_manhattan_dist(house_location, connect_location)

        if dist < min_dist: 
            nearest_connectpoint = connectpoint
            min_dist = dist
    
    return nearest_connectpoint


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

def order_vertical(objects_list):
    """
    Order batteries on vertical position
    """

    objects_list.sort(key=vertical_location, reverse=True)

def vertical_location(obj):
    """
    Returns vertical position of object
    """

    return obj.get_location()[1]
