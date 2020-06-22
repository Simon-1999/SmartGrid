import copy
from .algorithm import Algorithm

CAPACITY_OFFSET = 300

class DepthFirstLength(Algorithm):
    """
    A Depth First algorithm that builds a 
    """
    def __init__(self, district, clusters, n):
        self.district = district
        self.connections = self.remove_connections(self.district.connections)
        self.states = [copy.copy(self.connections)]
        self.clusters = clusters

        self.best_solution = None
        self.best_total = float('inf')
        self.longest_connection = float('inf')
        self.iterations = 0
        self.n = n
        self.process = []

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
            
            children.append([battery, house])
            
        self.add_best_children(connections, children, self.n)
        
    
    def check_solution(self, new_connections):
        """
        Checks and accepts better solutions than the current solution.
        """
        #print("solution")

        new_connection = self.get_longest_connection(new_connections)
        #print(new_connection)
        old_connection = self.longest_connection

        # update the cost if the district total is less
        if new_connection < old_connection:
            self.best_solution = new_connections
            self.longest_connection = new_connection
            total = self.calc_connection_costs(new_connections)

            # save the process
            solution = {"iter": self.iterations, "best_total": total, "longest_connection": self.longest_connection}
            self.process.append(solution)
            
            print(self.iterations)
            print(len(self.states))
            print(f"longest connection: {self.longest_connection}")
            print(f"New best value: {total}")

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
        # Update the input district with the best result found
        self.connections = self.best_solution

    
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
        print(f"amount of connections: {len(houses)}")
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

    

                
