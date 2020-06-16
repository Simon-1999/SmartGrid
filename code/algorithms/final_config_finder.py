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
        ITERATIONS = 10000
        min_costs = float('inf') 
        min_longest_connection_dist = float('inf') 
        best_connections = copy.copy(self.district.connections)  

        # set current_connections
        connections = {}
        for key, value in self.district.connections.items():
            connections[key] = copy.copy(value)

        # make random configurations
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

                # calculate longest cable
                longest_connection_dist = self.get_longest_connection(self.district.connections)

                # check if costs are better
                if longest_connection_dist < min_longest_connection_dist:
                    
                    # save new minimum value
                    min_longest_connection_dist = longest_connection_dist

                    # save connections in best connections
                    best_connections = {}
                    for key, value in self.district.connections.items():
                        best_connections[key] = copy.copy(value)    

            # reset district connections
            for key, value in connections.items():
                self.district.connections[key] = copy.copy(value)

        # set best connections
        self.district.connections = best_connections

        # results
        self.plot_connections(self.district, self.free_houses)
        self.print_result(self.district)

        print("ConfigFinder done ")

        return self.district        

    def nearest_free_battery(self, house):

        # sort clusters on distance from house
        self.clusters.sort(key=lambda cluster: self.calc_dist(cluster['centroid'], house.location))

        # chooses first free battery
        for cluster in self.clusters:

            if not self.district.calc_overload(cluster['battery'], house):
                return cluster['battery']

        return None

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
