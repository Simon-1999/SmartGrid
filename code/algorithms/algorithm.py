import copy

class Algorithm():

    def __init__(self, district):

        self.district = district
        self.iterations = 0

    def print_result(self, district):
        print("+---------------------------------+")
        if not district.is_overload() and district.all_houses_connected():
            print(f"| {'configuration:':<18} {'valid':>12} |")
        else:
            print(f"| {'configuration:':<18} {'invalid':>12} |")
        print(f"| {'iterations:':<18} {self.iterations:>12} |")
        costs = district.calc_connection_costs()
        print(f"| {'connections:':<18} {costs['connections']:>12} |")
        print(f"| {'batteries:':<18} {costs['batteries']:>12} |")
        print(f"| {'total:':<18} {costs['total']:>12} |")
        print("+---------------------------------+")  

    def calc_dist(self, location1, location2):

        x1, y1 = location1
        x2, y2 = location2

        return abs(x1 - x2) + abs(y1 - y2)

    def set_district_cables(self, district):
        """
        Sets the cables in a given district.
        """ 

        for battery in district.batteries:
            
            houses = district.connections[battery.id]

            for house in houses:

                path = self.get_path(house.location, battery.location)

                district.cables[house.id] = path


    def get_path(self, start_location, end_location):
        """ 
        Makes path of cable
        """  

        # unpack the locations
        current_x, current_y = start_location
        goal_x, goal_y = end_location

        # create path
        path = [(current_x, current_y)]

        # make horizontal path 
        while current_x < goal_x:
            current_x += 1
            path.append((current_x, current_y))

        while current_x > goal_x:
            current_x -= 1
            path.append((current_x, current_y))

        # make vertical path
        while current_y < goal_y:
            current_y += 1
            path.append((current_x, current_y))
 
        while current_y > goal_y:
            current_y -= 1
            path.append((current_x, current_y))

        return path    

        
