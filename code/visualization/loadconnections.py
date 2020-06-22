import csv

def load_connections(district, file_path):
    """
    Loads in district connections from a csv file
    """

    connections = {}

    with open(file_path, 'r') as in_file: 
        reader = csv.DictReader(in_file)

        for row in reader:
            battery_id = int(row["battery id"])
            connections[battery_id] = []

            house_ids = map(int, row["houses"].split(", "))

            for house_id in house_ids:

                for house in district.houses:

                    if house_id == house.id:
                        connections[battery_id].append(house)
    

    district.set_connections(connections)
    return district
