import copy
import random
import matplotlib.pyplot as plt
import numpy

from .algorithm import Algorithm

class ConfigFinder(Algorithm):

    def __init__(self, district, clusters):

        self.district = district
        self.clusters = clusters
        self.free_houses = []
        self.iterations = 0

    def run(self):
        
        print("ConfigFinder running...")

        CAPACITY_OFFSET = 350
        ITERATIONS = 50000
        min_costs = float('inf')
        longest_dist_length = float('inf')
        best_connections = copy.copy(self.district.connections)   

        found_costs = []

        # set current_connections
        connections = {}
        for key, value in self.district.connections.items():
            connections[key] = copy.copy(value)


        for i in range(ITERATIONS):

            # increment iterations
            self.iterations += 1

            # reset free houses
            self.free_houses = []

            # remove connections
            self.remove_connections(CAPACITY_OFFSET)

            # add connections
            self.add_connections()

            # check if solution is valid
            if self.district.all_houses_connected():

# ================= CODE FOR COST HEURISTIC ================
                # # calculate costs
                # costs = self.district.calc_connection_costs()['total']

                # # check if costs are better
                # if costs < min_costs:
                #     # save new minimum value
                #     min_costs = costs

# ================ CODE FOR LONGEST CABLE HEURISTIC =============
                # calculate longest connection
                length_sorted = []
                

                    # save connections in best connections
                    best_connections = {}
                    for key, value in self.district.connections.items():
                        best_connections[key] = copy.copy(value)    

            for key, value in connections.items():
                self.district.connections[key] = copy.copy(value)
            
            # calculate costs of the found configuration
            found_costs.append(min_costs)
            
            # update capacity for next run
            #print(f"decreasing capacity offset, current found cost: {min_costs}")
            #print(f"moving to iteration {i}")

        # set best connections
        self.district.connections = best_connections

        # results
        self.plot_connections(self.district, self.free_houses)
        self.print_result(self.district)

        # plot iterations vs. costs to visualize the decrease speed
        self.plot_iterations_cost_decrease(ITERATIONS, found_costs)

        # plot capacity offset vs. final costs
        #self.plot_offset_foundcosts(offsets, found_costs)

        return self.district        

    def nearest_free_battery(self, house):

        # sort clusters on distance from house
        self.clusters.sort(key=lambda cluster: self.calc_dist(cluster['centroid'], house.location))

        # chooses first free battery
        for cluster in self.clusters:

            if not self.district.calc_overload(cluster['battery'], house):
                return cluster['battery']

        return None

    def free_battery(self, house):
        """
        Equivalent to nearest_free_battery but without sorting based on distance
        """
        for cluster in self.clusters:
            if not self.district.calc_overload(cluster['battery'], house):
                return cluster['battery']


    def remove_connections(self, CAPACITY_OFFSET):

        # remove connections
        for battery in self.district.batteries:

            while self.district.get_usage(battery) > (battery.capacity - CAPACITY_OFFSET):

                # remove house
                removed_house = self.district.connections[battery.id].pop(0)

                # add removed hosue to free houses
                self.free_houses.append(removed_house)

    def add_connections(self):

        random.shuffle(self.free_houses)

        # connect free house to nearest free battery
        for house in self.free_houses:
            
            battery = self.nearest_free_battery(house)

            if battery != None:
                self.district.add_connection(battery, house)


    def add_random_connections(self):
        """
        Equivalent to add_connections(self), but chooses random battery with free capacity
        instead of using the nearness-heuristic
        """
        random.shuffle(self.free_houses)

        for house in self.free_houses:
            # find random battery that has capacity
            battery = self.free_battery(house)

            if battery != None:
                self.district.add_connection(battery, house)
                 

    def plot_connections(self, district, free_houses):

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1) 
        plt.title(f'District{district.id}')

        color = {0: "blue", 1:"red" ,2:"yellow",3:"cyan", 4:"magenta"} 

        # loop through batteries
        for battery in district.batteries:
            x, y = battery.location
            plt.plot(x, y, 'ks', label = f'battery{battery.id}', color=color[battery.id], markersize=10)

            for house in district.connections[battery.id]:             
                x, y = house.location
                plt.plot(x, y, 'p', color=color[battery.id], markersize=7, alpha=0.5)

        for free_house in free_houses:
            x, y = free_house.location
            plt.plot(x, y, 'kp', markersize=15, alpha=0.1)

        # plot district  
        ax.set_xticks(numpy.arange(0, 51, 1), minor=True)
        ax.set_yticks(numpy.arange(0, 51, 1), minor=True)
        ax.grid(which='minor', alpha=0.2)
        plt.legend()
        plt.show()



    def plot_offset_foundcosts(self, offsets, found_costs):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        plt.title(f"Costs of district after changing capacity offsets")

        ax.plot(offsets, found_costs)
        plt.show()

    def plot_iterations_cost_decrease(self, iters, found_costs):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        plt.title(f"Costs of district after every iteration of ConfigFinder")

        ax.plot(list(range(iters)), found_costs)

        axes = plt.gca()
        axes.set_ylim([57000,61000])

        plt.show()