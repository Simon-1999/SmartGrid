"""Our K-Means DepthFirstCosts algorithm performs on a K-Means sorted district. It determines houses to check
based on a capacity offset. These are removed from the batteries, to create free space to switch houses in.
The algorithm then does a depth first search for the best configuration based on the minimal cost of a state it can find by
reassigning all free houses. 
Pruning is done by selecting the two best options of the five diversions from every branch. 
"""

import copy
from .algorithm import Algorithm

CAPACITY_OFFSET = 200
N = 2

class DepthFirstCosts(Algorithm):
    """
    A Depth First algorithm that builds a 
    """
    def __init__(self, district):
        self.district = copy.deepcopy(district)
        self.connections = self.remove_connections(self.district.connections)
        self.states = [copy.copy(self.connections)]
        self.best_solution = None
        self.best_total = float('inf')
        self.iterations = 0

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
        batteries = self.district.get_possible_batteries(house)

        children = []

        # add an instance to the stack with each possible battery connection
        for battery in batteries:

            # copy connections
            new_connections = {}
            for key, value in connections.items():
                new_connections[key] = copy.copy(value)
        
            new_connections[battery.id].append(house)
            children.append(new_connections)

        best_children = self.get_best_child(children, N)
        self.states += best_children
        
    
    def check_solution(self, new_connections):
        """
        Checks and accepts better solutions than the current solution.
        """

        res = self.district.calc_connection_costs()
        new_total = res["total"]
        
        old_total = self.best_total

        # update the cost if the district total is less
        if new_total <= old_total:
            self.best_solution = new_connections
            self.best_total = new_total

    def run(self):
        """
        Runs the algorithm untill all possible states are visited.
        """
    
        while self.states:
            new_connections = self.get_next_state()

            # set the district connections
            self.district.set_connections(new_connections)

            # retrieve the next empty house
            house = self.district.get_empty_house()

            if house is not None:
                self.build_children(new_connections, house)
                
            else:

                # continue looking for better districts.
                self.check_solution(new_connections)

            self.iterations += 1
            
        # update the input district with the best result found
        self.district.set_connections(self.best_solution)

        return self.district
    


    def get_best_child(self, children, n):
        """
        Returns the child state with the lowest cost
        """

        children.sort(key=lambda connections: self.calc_connection_costs(connections))

        return children[:n]

    
    def remove_connections(self, connections):

        # remove connections
        for battery in self.district.batteries:

            while self.district.get_usage(battery) > (battery.capacity - CAPACITY_OFFSET):

                # remove house
                house = connections[battery.id].pop(0)
                self.district.houses.remove(house)
                self.district.houses.insert(0, house)
                
        houses = []
        for value in connections.values():
            houses += value

        return connections

    def calc_battery_connections_costs(self,connections, battery):
        """
        Calculates costs of connection to battery
        """

        houses = connections[battery.id]
        costs = 0

        for house in houses:
            costs += self.calc_dist(house.location, battery.location) * 9

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

        costs =  connections_cost + batt_cost

        return costs

                
