import copy

class DepthFirst:
    """
    A Depth First algorithm that builds a 
    """
    def __init__(self, district):
        self.district = copy.deepcopy(district)
        self.connections = self.district.connections
        self.states = [copy.copy(self.connections)]

        self.best_solution = None
        self.best_total = float('inf')
        self.iter = 0

    def get_next_state(self):
        """
        Get next state from the back of the stack
        """

        return self.states.pop()

    def build_children(self, connections, house):
        """
        Creates all possible child-states and adds them to the list of states.
        """

        # retrieves all free batteries the house can connect to
        batteries = self.get_possible_batteries(connections, house)


        # add an instance to the stack with each possible battery connection
        for battery in batteries:
            new_connections = {}

            for key, value in connections.items():
                new_connections[key] = copy.copy(value)

            self.add_connection(new_connections, battery, house)
            #print("==========New Child==========")
            #print(new_connections)
            #print("==========New Child==========")
            self.states.append(new_connections)
        
    
    def check_solution(self, new_connections):
        """
        Checks and accepts better solutions than the current solution.
        """

        res = self.calc_connection_costs(new_connections)
        new_total = res["total"]
        
        old_total = self.best_total

        # update the cost if the district total is less
        if new_total <= old_total:
            self.best_solution = new_connections
            self.best_total = new_total
            print(self.iter)
            print(len(self.states))
            print(f"New best value: {self.best_total}")

    def run(self):
        """
        Runs the algorithm untill all possible states are visited.
        """
    
        for i in range(5000):#while self.states:
            #print(f"===============New State, statelength: {len(self.states)}==============")
            new_connections = self.get_next_state()

            self.iter += 1

            # retrieve the next empty house
            house = self.get_empty_house(new_connections)

            #print("HOUSE")
            #print(house)
            #print("=======")

            #print(house)

            if house is not None:
                self.build_children(new_connections, house)

                #print("=========Stateslist==========")
                #for state in self.states:
                    #print("======A single state=====")
                    #print(state.batteries)
                #print("=========Stateslist==========")
                
            else:
                # stop if we find a solution
                #self.connections = new_connections
                #return

                # continue looking for better districts.
                self.check_solution(new_connections)

        # Update the input district with the best result found
        self.connections = self.best_solution

    def get_empty_house(self, connections):
        """
        Returns an empty house
        """

        connected_houses = []
        for values in connections.values():
            connected_houses += values

     
        for house in self.district.houses:
            if house not in connected_houses:
                return house
        
        return None

    def get_possible_batteries(self, connections, house):
        """
        Returns a list of batteries a house can connect to
        """
        empty_batteries = []
        for battery in self.district.batteries:
            if not self.calc_overload(connections, battery, house):
                empty_batteries.append(battery)
        
        return empty_batteries

    def calc_overload(self, connections, battery, house):
        """
        Returns if house output exceeds battery capacity
        """

        return self.get_usage(connections, battery) + house.output > battery.capacity


    def get_usage(self, connections, battery):
        """
        Gets the battery usage form the connections list
        """

        houses = connections[battery.id]
        usage = 0

        for house in houses:
            usage += house.output

        return usage

    def add_connection(self, connections, battery, house):
        """
        Connect house to battery
        """

        connections[battery.id].append(house)

    def calc_battery_connections_costs(self,connections, battery):
        """
        Calculates costs of connection to battery
        """

        houses = connections[battery.id]
        costs = 0

        for house in houses:
            costs += self.calc_dist(house, battery) * 9

        return costs

    def calc_connection_costs(self, connections):
        """
        Calculates the total cost of the district
        """

        connections_cost = 0
        batt_cost = 0

        for battery in self.district.batteries:
            batt_cost += battery.cost
            connections_cost += self.calc_battery_connections_costs(connections, battery)

        costs = {
            "connections": connections_cost,
            "batteries": batt_cost,
            "total": connections_cost + batt_cost
        }

        return costs

    def calc_dist(self, object1, object2):
        """
        Calculates manhatten distance between two objects
        """

        x1, y1 = object1.location
        x2, y2 = object2.location

        return abs(x1 - x2) + abs(y1 - y2) 

                