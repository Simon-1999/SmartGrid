import json

def output_doc(district, shared):
    """
    Writes a District object to a .json output file. 

    Parameters
    ----------
    district : District object
        Configuration of the district to write output for

    shared : bool
        Whether the cables are unique or shared in the district
    """

    # create a list to store all the data in
    data = []

    # start with the first item in the dictionary; general district info
    district_info = {}
    district_info['district'] = district.id
    if shared:
        district_info['shared-costs'] = district.calc_connection_costs()['total']
    else:
        district_info['own-costs'] = district.calc_connection_costs()['total']

    data.append(district_info)

    # loop through every battery in the district
    for battery in district.get_batteries():
        battery_data = {}

        # create general info for each battery
        battery_data['location'] = battery.location
        battery_data['capacity'] = battery.capacity
        battery_data['houses'] = []

        data.append(battery_data)

        # loop through every house in the district
        for house in district.connections[battery.id]:

            # store house information in dictionary
            house_info = {}

            house_info['location'] = house.location
            house_info['output'] = house.output
            house_info['cables'] = district.cables[house.id]

            # add house dict to battery
            battery_data['houses'].append(house_info)

    # write everything to output file
    with open("output.json", "w+") as outfile:
        json.dump(data, outfile)
