import csv

def load_connections(district, file_path):
    """
    Loads in district connections from a csv file

    Parameters
    ----------
    file_path : str
        csv file path

    Return
    ----------
    District object
        District with loaded connections

    """

    connections = {}

    # open the csv file
    with open(file_path, 'r') as in_file: 
        reader = csv.DictReader(in_file)

        # loop through the rows
        for row in reader:
            battery_id = int(row["battery id"])
            connections[battery_id] = []

            house_ids = map(int, row["houses"].split(", "))

            # create the connections dictionary
            for house_id in house_ids:

                for house in district.houses:

                    if house_id == house.id:
                        connections[battery_id].append(house)
    
    # set the connections in the district
    district.set_connections(connections)
    
    return district
