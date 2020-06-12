import copy

class Algorithm():

    def __init__(self, district):

        self.district = copy.deepcopy(district) 
        self.iterations = 0

    def print_result(self, district):
        print("+---------------------------------+")
        if not district.is_overload() and district.all_houses_connected():
            print(f"| {'configuration:':<18} {'valid':>12} |")
        else:
            print(f"| {'configuration:':<18} {'invalid':>12} |")
            for house in district.get_houses():
                if not house.has_cable():
                    x, y = house.get_location()
                    print(f"| house at [{x}, {y}] {'not connected':>12} |")
        print(f"| {'iterations:':<18} {self.iterations:>12} |")
        costs = district.calc_costs()
        print(f"| {'cables:':<18} {costs['cables']:>12} |")
        print(f"| {'batteries:':<18} {costs['batteries']:>12} |")
        print(f"| {'total:':<18} {costs['total']:>12} |")
        print("+---------------------------------+")  

    def calc_dist(self, location1, location2):

        x1, y1 = location1
        x2, y2 = location2

        return abs(x1 - x2) + abs(y1 - y2)    