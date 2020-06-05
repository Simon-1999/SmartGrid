
def cable_path(house_location, battery_location):
    # unpack the locations into variables
    house_x, house_y = house_location
    batt_x, batt_y = battery_location

    # set current location and goal location
    current_x = min(house_x, batt_x) 
    goal_x = max(house_x, batt_x)
    current_y = min(house_y, batt_y)
    goal_y = max(house_y, batt_y)

    # create path
    path = [(current_x, current_y)]

    # loop through path horizontally and vertically respectively
    while current_x < goal_x:
        current_x += 1
        path.append((current_x, current_y))

    while current_y < goal_y:
        current_y += 1
        path.append((current_x, current_y))

    return path


test_house = (4, 12)
test_battery = (1, 1)

print(cable_path(test_house, test_battery))