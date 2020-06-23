"""This algorithm performs on a K-Means sorted district. It determines houses to checkbased on a capacity offset. 
These are removed from the batteries, to create free space to switch houses in.
The algorithm then randomly connects the free houses to the battery and calculates the total district cost.
It does this over multiple iterations and eventually returns the district with the cheapest configuration.
"""

import copy
import random

from .algorithm import Algorithm

CAPACITY_OFFSET = 350
ITERATIONS = 50000 

class ConfigFinderCosts(Algorithm):
    """Explores different district configuratiom by removing a set of houses that are on the border of the formed clusters
    and randomly reassigns them to batteries over multiple iterations. Returns the configuration with the lowest cost.

    Attributes
    ----------
    district: District object
        A district clustered and sorted through a kmeans algorithm

    clusters: list
        Dictionaries with cluster centroid locations,
        lists of houses in the cluster 
        and the Battery objects

    free_houses: list
        House objects without connections

    min_costs: float
        Lowest configuration cost found
    
    best_connections: dict
        Found configuration with the lowest cost

    Methods
    ----------

    run()
        Runs the algorithm

    nearest_free_battery(house)
        Finds battery belonging the closest cluster to a house

    remove_connections(CAPACITY_OFFSET)
        Removes connections with a specified capacity offset

    add_connections()
        Randomly assigns connections between free houses and batteries

    """

    def __init__(self, district, clusters):
        """Parameters
        ----------
        district : District object
            District to perform actions on
        
        clusters : list
            information about the the clusters
        """

        self.district = district
        self.clusters = clusters
        self.free_houses = []
        self.min_costs = float('inf')
        self.best_connections = copy.copy(self.district.connections)   


    def run(self):
        """Runs the ConfigFinderCosts algorithm

        Returns
        ----------
        District object
            Cheapest district configuration found over the iterations
        """
        
        # prompt the user for iterations
        iterations = self.prompt_iterations(default=ITERATIONS)

        # save initial connections
        init_connections = {}
        for key, value in self.district.connections.items():
            init_connections[key] = copy.copy(value)

        for i in range(iterations):
            
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
                    # save new minimum value
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
        """
        Calculates which battery belongs to the cluster nearest to the given house

        Paramaters
        ----------
        house : House object

        Returns
        ----------
        Battery object
        """

        # sort clusters on distance from house
        self.clusters.sort(key=lambda cluster: self.calc_dist(cluster['centroid'], house.location))

        # chooses first free battery
        for cluster in self.clusters:

            if not self.district.calc_overload(cluster['battery'], house):
                return cluster['battery']

        return None


    def remove_connections(self, CAPACITY_OFFSET):
        """ Subtracts a specified offset from each battery and removes house connections from that battery 
        untill the offset is reached. Removed houses are stored in the free houses list.

        Paramaters
        ----------
        CAPACITY_OFFSET : int
        """

        # remove connections
        for battery in self.district.batteries:

            while self.district.get_usage(battery) > (battery.capacity - CAPACITY_OFFSET):

                # remove house
                removed_house = self.district.connections[battery.id].pop(0)

                # add removed hosue to free houses
                self.free_houses.append(removed_house)


    def add_connections(self):
        """ Randomly shuffles the list of free houses and adds connections between the free houses
        and the nearest batteries with enough capacity.
        """

        random.shuffle(self.free_houses)

        # connect free house to nearest free battery
        for house in self.free_houses:
            
            battery = self.nearest_free_battery(house)

            if battery != None:
                self.district.add_connection(battery, house)