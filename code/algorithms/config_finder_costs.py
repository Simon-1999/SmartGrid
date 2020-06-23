"""
"""

import copy
import random
import matplotlib.pyplot as plt
import numpy

from .algorithm import Algorithm


CAPACITY_OFFSET = 350
ITERATIONS = 50000 

class ConfigFinderCosts(Algorithm):

    def __init__(self, district, clusters):

        self.district = district
        self.clusters = clusters
        self.free_houses = []
        self.iterations = 0
        self.min_costs = float('inf')
        self.best_connections = copy.copy(self.district.connections)   

    def run(self):
        
        # prompt the user for iterations
        iterations = self.prompt_iterations(default=ITERATIONS)

        # save initial connections
        init_connections = {}
        for key, value in self.district.connections.items():
            init_connections[key] = copy.copy(value)


        for i in range(iterations):

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

                # calculate costs
                costs = self.district.calc_connection_costs()['total']

                # check if costs are better
                if costs < self.min_costs:
                    #save new minimum value
                    self.min_costs = costs
                    self.best_connections = self.district.connections

            # reset the initial connections
            connections = {}
            for key, value in init_connections.items():
                connections[key] = copy.copy(value)
            
            # set connections
            self.district.set_connections(connections)


        # set best connections
        self.district.set_connections(self.best_connections)

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
                 
