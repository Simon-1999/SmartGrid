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
        batteries = self.district.get_possible_batteries(house)


        # add an instance to the stack with each possible battery connection
        for battery in batteries:

            new_connections = {}
            for key, value in connections.items():
                new_connections[key] = copy.copy(value)

            new_connections[battery.id].append(house)
            self.states.append(new_connections)
            print("============NEW STATE============")
            print(new_connections)
        
    
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
            print(self.iter)
            print(len(self.states))
            print(f"New best value: {self.best_total}")

    def run(self):
        """
        Runs the algorithm untill all possible states are visited.
        """
    
        for i in range(10):#while self.states:
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

            self.iter += 1

        # Update the input district with the best result found
        self.connections = self.best_solution