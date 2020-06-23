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
    """A Depth First algorithm that selects houses that are close to clusters other than their own, and
    disconnects those from their batteries until the capacity offset is reached. It then performs a depth first
    search for the best configuration. Pruning is done by selecting the two best options of the five diversions from 
    every branch.

    Parameters
    ----------
    district : District object

    Methods
    ----------
    run()
        Runs the algorithm.

    get_next_state()
        Get next state from the back of the stack.

    build_children(connections, house)
        Creates all possible child-states and adds them to the list of states.

    check_solution(new_connections)
        Checks for the best solution and accepts that state.

    remove_connections(connections)
        Remove connections from a district

    calc_battery_connection_costs(connections, battery)
        Calculates costs of connection to one battery.

    calc_connection_costs(connections)
        Calculates the total cost of the district.
    
    get_longest_connection(connections)
        Returns the maximum connection distance in a cluster.

    get_connection_len(battery, house)
        Calculates distance of a house to a cluster centroid.

    add_best_children(connections, children, n)
        Adds the pruned child states to the stack.
    """

    def __init__(self, district, clusters):
        """Parameters
        ----------
        district : District object

        clusters : list
            Formed clusters in the district

        """
        self.district = district
        self.connections = self.remove_connections(self.district.connections)
        self.states = [copy.copy(self.connections)]
        self.clusters = clusters

        self.best_solution = None
        self.best_total = float('inf')
        self.longest_connection = float('inf')
        self.iterations = 0

    def run(self):
        """Runs the algorithm untill all possible states are visited.

        Returns
        ----------
        District object
            Best found configuration
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
        """Get next state from the back of the stack.

        Returns
        ----------
        dict
        """

        return self.states.pop()

    def build_children(self, connections, house):
        """Creates all possible child-states and adds them to the list of states.

        Parameters
        ----------
        connections : dict

        house : House object
        """

        # retrieves all free batteries the house can connect to
        batteries = self.district.get_possible_batteries(house)

        children = []
        # add an instance to the stack with each possible battery connection
        for battery in batteries:
            
            children.append([battery, house])
            
        self.add_best_children(connections, children, N)
        
    
    def check_solution(self, new_connections):
        """Checks and accepts better solutions than the current solution.

        Parameters
        ----------
        new_connections : dict

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
        """Removes connections from a district.

        Parameters
        ----------
        connections : dict

        Returns
        ----------
        dict
        """

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
        """Calculates costs of connection to one battery.

        Parameters
        ----------
        connections : dict

        battery : Battery object

        Returns
        ----------
        float
        """

        connections_cost = 0
        batt_cost = 0

        for battery in self.district.batteries:
            batt_cost += battery.cost
            connections_cost += self.calc_battery_connections_costs(connections, battery)

        costs =  connections_cost + batt_cost

        return costs

    def get_longest_connection(self, connections):
        """Returns the maximum connection distance in a cluster.

        Parameters
        ----------
        connections : dict

        Returns
        ----------
        float
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
        """Calculates distance of a house to a cluster centroid of a certain batteries' cluster

        Parameters
        ----------
        battery : Battery object

        house : House object

        Returns
        ----------
        float
        """

        cluster = self.clusters[battery.id]
        centroid = cluster["centroid"]
        
        return self.calc_dist(centroid, house.location)

    def add_best_children(self,connections, children, n):
        """Adds the pruned child states to the stack.

        Parameters
        ----------
        connections : dict

        children : list
            New district states to evaluate
        
        n : int
            Amount of pruning to do
        """
        children.sort(key=lambda temp: self.get_connection_len(temp[0], temp[1]))

        for battery, house in children[:n]:
    
            # copy connections
            new_connections = {}
            for key, value in connections.items():
                new_connections[key] = copy.copy(value)

            new_connections[battery.id].append(house)
            self.states.append(new_connections)

    

                

        
