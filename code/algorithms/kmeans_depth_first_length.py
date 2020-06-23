"""Our K-Means DepthFirstLength algorithm performs on a K-Means sorted district. It determines houses to check
based on a capacity offset. These are removed from the batteries, to create free space to switch houses in.
The algorithm then does a depth first search for the best configuration based on the shortest maximum cable it can find by
reassigning all free houses. 
Pruning is done by selecting the two best options of the five diversions from every branch. 
"""

import copy
from .algorithm import Algorithm

CAPACITY_OFFSET = 300
N = 2

class DepthFirstLength(Algorithm):
    """
    Does a depth first search for the best district based on the maximum longest cable it finds by reassigning
    houses that are on the border of formed clusters. 

    Methods
    ----------
    run()

    get_next_state()

    build_children(connections, house)

    check_solution()

    remove_connections(connections)

    calc_battery_connections_costs(connections, battery)

    calc_connection_costs(connections)

    get_longest_connection(connections)

    get_connection_len(battery, house)

    add_best_children(self,connections, children, n)

    """

    def __init__(self, district, clusters):
        """Parameters
        ----------
        district : District object

        clusters : list
            Formed clusters in the district

        """
        self.district = copy.deepcopy(district)
        self.connections = self.remove_connections(self.district.connections)
        self.states = [copy.copy(self.connections)]
        self.clusters = clusters

        self.best_solution = None
        self.best_total = float('inf')
        self.longest_connection = float('inf')
        self.iterations = 0

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
    
    def get_next_state(self):
        """Get next state from the top of the stack.
        """

        return self.states.pop()

    def build_children(self, connections, house):
        """Creates all possible child-states and adds them to the list of states.

        Parameters
        ----------
        connections : dict ?????

        house : House object
            House to build children for based on connection possibilities
        """

        # retrieves all free batteries the house can connect to
        batteries = self.district.get_possible_batteries(house)

        children = []
        # add an instance to the stack with each possible battery connection
        for battery in batteries:
            
            children.append([battery, house])
            
        self.add_best_children(connections, children, N)
        
    
    def check_solution(self, new_connections):
        """Checks and accepts better solutions into the state stack than the current solution.
        """
        

        new_connection = self.get_longest_connection(new_connections)
        old_connection = self.longest_connection

        # update the cost if the district total is less
        if new_connection < old_connection:
            self.best_solution = new_connections
            self.longest_connection = new_connection
            total = self.calc_connection_costs(new_connections)

            # save the process
            solution = {"iter": self.iterations, "best_total": total, "longest_connection": self.longest_connection}

    
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

    def get_longest_connection(self, connections):
        """Returns the maximum distance in a cluster.
        """

        max_dist = 0

        # loop through clusters
        for cluster in self.clusters:

            # loop through houses in cluster
            for house in connections[cluster['battery'].id]:

                dist = self.calc_dist(house.location, cluster['centroid'])

                # save maximum distance
                if dist > max_dist:
                    max_dist = dist

        return max_dist

    def get_connection_len(self, battery, house):

        cluster = self.clusters[battery.id]
        centroid = cluster["centroid"]
        
        return self.calc_dist(centroid, house.location)

    def add_best_children(self,connections, children, n):
        children.sort(key=lambda temp: self.get_connection_len(temp[0], temp[1]))

        for battery, house in children[:n]:
    
            # copy connections
            new_connections = {}
            for key, value in connections.items():
                new_connections[key] = copy.copy(value)

            new_connections[battery.id].append(house)
            self.states.append(new_connections)

    

                
